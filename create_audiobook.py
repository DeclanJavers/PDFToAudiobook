import os
import re
import shutil
from pdfminer.high_level import extract_text
from kokoro import KPipeline
import soundfile as sf
from pydub import AudioSegment

def extract_text_from_pdf(pdf_path):
    print(f"Extracting text from PDF: {pdf_path}")
    return extract_text(pdf_path)

def split_into_chunks(text, target_length=500):
    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= target_length:
            current_chunk = f"{current_chunk} {sentence}".strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def initialize_kokoro_pipeline():
    print("Initializing Kokoro pipeline")
    return KPipeline(lang_code='a')

def generate_and_save_audio(pipeline, text, output_dir='.'):
    print("Generating and saving audio files")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    chunks = split_into_chunks(text, target_length=500)
    total_chunks = len(chunks)
    print(f"Total chunks to process: {total_chunks}")
    combined_audio = AudioSegment.silent(duration=0)
    file_index = 0
    for idx, chunk in enumerate(chunks):
        generator = pipeline(chunk, voice='af_heart', speed=1, split_pattern=None)
        for gs, ps, audio in generator:
            file_name = os.path.join(output_dir, f'{file_index}.wav')
            sf.write(file_name, audio, 24000)
            audio_segment = AudioSegment.from_wav(file_name)
            combined_audio += audio_segment
            print(f"Processed segment {file_index}")
            file_index += 1
        chunks_remaining = total_chunks - (idx + 1)
        percent_complete = ((idx + 1) / total_chunks) * 100
        print(f"Chunk {idx + 1}/{total_chunks} complete. {chunks_remaining} chunks remaining ({percent_complete:.1f}% done).")
    return combined_audio

def combine_audios_to_file(combined_audio, output_path='audiobook.wav'):
    print("Combining audio segments into audiobook")
    combined_audio.export(output_path, format='wav')

if __name__ == "__main__":
    input_dir = './input'
    output_base_dir = './audio_files'
    final_output_dir = './audiobooks'
    
    if not os.path.exists(final_output_dir):
        os.makedirs(final_output_dir)
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the input directory.")
    else:
        pipeline = initialize_kokoro_pipeline()
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            pdf_name = os.path.splitext(pdf_file)[0]
            output_dir = os.path.join(output_base_dir, pdf_name)
            output_audio_file = os.path.join(final_output_dir, f"{pdf_name}.wav")
            
            print(f"Processing PDF: {pdf_file}")
            text = extract_text_from_pdf(pdf_path)
            combined_audio = generate_and_save_audio(pipeline, text, output_dir)
            combine_audios_to_file(combined_audio, output_path=output_audio_file)
            
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
                print(f"Deleted temporary directory: {output_dir}")
            
            print(f"Completed processing {pdf_file}. Output saved to {output_audio_file}")