import json

def normalize_frames(input_file, output_file):
    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Process each word in the dictionary
    for word in data:
        frames = data[word]
        
        # Sort frames by frame number
        frames.sort(key=lambda x: x['Frame'])
        
        # Normalize frame numbers to start from 0
        for i, frame in enumerate(frames):
            frame['Frame'] = i

    # Write the normalized data to output file
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Frame numbers normalized and saved to {output_file}")

if __name__ == "__main__":
    input_file = "static/json/reference1.json"
    output_file = "static/json/reference1_normalized.json"
    normalize_frames(input_file, output_file)