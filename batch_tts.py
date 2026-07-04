#!/usr/bin/env python3
"""批量生成博弈论51份课程内容TTS音频"""
import os, re, sys, subprocess, asyncio, time
from pathlib import Path

COURSES_DIR = os.path.expanduser("~/Desktop/OPC/game-theory-academy/docs/courses")
OUTPUT_DIR = os.path.expanduser("~/Desktop/OPC/game-theory-academy/audio")
VOICE = "zh-CN-YunxiNeural"  # 中文男声，清晰专业
CHUNK_SIZE = 3500  # 每段字符数
MAX_RETRIES = 3

def strip_markdown(text):
    """去除markdown标记，保留可读文本"""
    # 移除代码块
    text = re.sub(r'```[\s\S]*?```', '', text)
    # 移除行内代码
    text = re.sub(r'`[^`]+`', '', text)
    # 移除图片
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # 移除链接，保留文字
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # 移除加粗/斜体标记
    text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 表格转为可读格式
    text = re.sub(r'\|', '，', text)
    text = re.sub(r'[-]{3,}', '', text)
    # 移除多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 标题保留
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # 移除">"引用标记
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    # 移除多余空白
    text = re.sub(r' +', ' ', text)
    return text.strip()

def split_text(text, max_chars=CHUNK_SIZE):
    """将文本按句子边界分割成块"""
    chunks = []
    current = ""
    # 按句子分割
    sentences = re.split(r'(?<=[。！？.!?])\s*', text)
    
    for sentence in sentences:
        if not sentence.strip():
            continue
        if len(current) + len(sentence) < max_chars:
            current += sentence
        else:
            if current.strip():
                chunks.append(current.strip())
            current = sentence
    
    if current.strip():
        chunks.append(current.strip())
    
    return chunks

async def generate_tts(text, output_path, voice=VOICE):
    """生成单个TTS文件"""
    for attempt in range(MAX_RETRIES):
        try:
            cmd = [
                "edge-tts",
                "--text", text,
                "--voice", voice,
                "--write-media", output_path,
                "--rate", "+10%"  # 稍快语速
            ]
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode == 0 and os.path.getsize(output_path) > 100:
                return True
            else:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(2)
                else:
                    print(f"  FAILED after {MAX_RETRIES} attempts: {stderr.decode()[:200]}")
                    return False
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(2)
            else:
                print(f"  ERROR: {e}")
                return False
    return False

def concat_mp3s(input_files, output_file):
    """用ffmpeg拼接多个MP3"""
    if len(input_files) == 1:
        os.rename(input_files[0], output_file)
        return True
    
    # 创建文件列表
    list_file = output_file + ".txt"
    with open(list_file, "w") as f:
        for mp3 in input_files:
            f.write(f"file '{os.path.abspath(mp3)}'\n")
    
    try:
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", list_file, "-c", "copy", output_file
        ], capture_output=True, check=True)
        os.remove(list_file)
        # 清理分块
        for mp3 in input_files:
            os.remove(mp3)
        return True
    except Exception as e:
        print(f"  CONCAT ERROR: {e}")
        return False

async def process_course(md_path, output_dir):
    """处理单个课程"""
    course_name = os.path.splitext(os.path.basename(md_path))[0]
    # 清理文件名
    safe_name = re.sub(r'[^\w\-]', '_', course_name)
    output_file = os.path.join(output_dir, f"{safe_name}.mp3")
    chunks_dir = os.path.join(output_dir, "_chunks", safe_name)
    
    print(f"\n📖 {course_name}")
    
    # 读取markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # 提取纯文本
    plain_text = strip_markdown(md_text)
    if len(plain_text) < 100:
        print(f"  ⚠️ 文本太短({len(plain_text)}字符)，跳过")
        return None
    
    # 分割
    chunks = split_text(plain_text)
    print(f"  📝 {len(plain_text)}字符 → {len(chunks)}段")
    
    # 生成每段TTS
    os.makedirs(chunks_dir, exist_ok=True)
    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_path = os.path.join(chunks_dir, f"chunk_{i:03d}.mp3")
        sys.stdout.write(f"  🔊 段{i+1}/{len(chunks)}... ")
        sys.stdout.flush()
        success = await generate_tts(chunk, chunk_path)
        if success:
            chunk_files.append(chunk_path)
            print("✅")
        else:
            print("❌")
    
    if not chunk_files:
        print(f"  ❌ 全部失败")
        return None
    
    # 拼接
    print(f"  🔗 拼接 {len(chunk_files)} 段...")
    if concat_mp3s(chunk_files, output_file):
        # 清理chunks目录
        try:
            os.rmdir(chunks_dir)
        except:
            pass
        size_mb = os.path.getsize(output_file) / (1024*1024)
        print(f"  ✅ 完成: {size_mb:.1f}MB")
        return output_file
    else:
        print(f"  ❌ 拼接失败")
        return None

async def main():
    start_time = time.time()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 获取所有课程文件，按编号排序
    md_files = sorted(
        [f for f in os.listdir(COURSES_DIR) if f.endswith('.md')],
        key=lambda x: int(re.match(r'(\d+)', x).group(1)) if re.match(r'(\d+)', x) else 999
    )
    
    print(f"🎙️ 批量TTS生成开始")
    print(f"📂 课程目录: {COURSES_DIR}")
    print(f"📂 输出目录: {OUTPUT_DIR}")
    print(f"🎤 语音: {VOICE}")
    print(f"📚 课程数: {len(md_files)}")
    print(f"{'='*50}")
    
    completed = []
    failed = []
    
    for i, md_file in enumerate(md_files):
        path = os.path.join(COURSES_DIR, md_file)
        print(f"\n[{i+1}/{len(md_files)}]", end="")
        result = await process_course(path, OUTPUT_DIR)
        if result:
            completed.append(result)
        else:
            failed.append(md_file)
        
        # 短暂休息避免请求过快
        await asyncio.sleep(1)
    
    elapsed = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"🎉 完成! {len(completed)}成功 / {len(failed)}失败 / 总耗时{elapsed/60:.1f}分钟")
    
    if failed:
        print(f"❌ 失败: {', '.join(failed)}")
    
    # 总大小
    total_size = sum(os.path.getsize(f) for f in completed) / (1024*1024)
    print(f"💾 总大小: {total_size:.1f}MB")

if __name__ == "__main__":
    asyncio.run(main())
