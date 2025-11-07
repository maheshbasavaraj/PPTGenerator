import video_processing
import ppt_generator
import os
import sys

def main():
    video_path = "C:\\Mahesh\\AI projects\\pptgen\\uploads\\S2S.mp4" # This will be replaced by the user's input
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    
    if not os.path.exists(video_path):
        print("Error: Video file not found.")
        return

    method_choice = '1'
    if method_choice == '1':
        ssim_threshold = 0.98
        image_paths = video_processing.extract_key_frames(video_path, ssim_threshold=ssim_threshold)
    elif method_choice == '2':
        try:
            diff_threshold = int(input("Enter the difference threshold (e.g., 25): "))
        except ValueError:
            print("Invalid input. Using default difference threshold (25).")
            diff_threshold = 25
        image_paths = video_processing.extract_frames_by_difference(video_path, threshold=diff_threshold)
    else:
        print("Invalid choice. Using default SSIM method with threshold 0.98.")
        image_paths = video_processing.extract_key_frames(video_path, ssim_threshold=0.98)

    output_filename = os.path.splitext(os.path.basename(video_path))[0] + ".pptx"
    
    print(f"Processing video: {video_path}")
    
    if image_paths:
        print(f"Extracted {len(image_paths)} key frames.")
        texts = [f"This is slide {i+1}" for i in range(len(image_paths))]
        
        output_path = os.path.join("generated", output_filename)
        print(f"Generating PowerPoint presentation at {output_path}...")
        ppt_generator.create_ppt(image_paths, texts, output_path)
        
        print(f"PowerPoint presentation generated successfully at {output_path}")
    else:
        print("No key frames were extracted.")

if __name__ == "__main__":
    main()

