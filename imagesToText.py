import Quartz
from Foundation import NSURL
import Vision
import os

# Global list to store all results from images
all_results = []

def recognize_text_handler(request, error):
    observations = request.results()
    results = []
    for observation in observations:
        # Return the string of the top VNRecognizedText instance.
        recognized_text = observation.topCandidates_(1)[0]
        results.append([recognized_text.string(), recognized_text.confidence()])
    # Append results from this image to global results
    all_results.append(results)
    return None  # This ensures the handler returns None as expected by Vision


def process_images_in_folder(folder_path):
    # List all images in the specified folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith(".png")]

    # Process each image and recognize text
    for image_file in sorted(image_files):
        img_path = os.path.join(folder_path, image_file)

        # Get the CIImage on which to perform requests.
        input_url = NSURL.fileURLWithPath_(img_path)
        input_image = Quartz.CIImage.imageWithContentsOfURL_(input_url)

        # Create a new image-request handler.
        request_handler = Vision.VNImageRequestHandler.alloc().initWithCIImage_options_(
            input_image, None
        )

        # Create a new request to recognize text.
        request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(recognize_text_handler)

        # Perform the text-recognition request.
        request_handler.performRequests_error_([request], None)


def write_results_to_file(output_file):
    with open(output_file, "w") as f:
        for result_set in all_results:
            for result in result_set:
                recognized_text = result[0]
                f.write(recognized_text + "\n")


# Folder containing the images and output file path
image_folder = "pdf_images/sample_pdf_images"
output_text_file = "output_text.txt"

# Process all images in the folder
process_images_in_folder(image_folder)

# Write all recognized text to the output file
write_results_to_file(output_text_file)