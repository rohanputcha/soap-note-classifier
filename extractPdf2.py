import Quartz
from Foundation import NSURL
import Vision


def recognize_text_handler(request, error):
    observations = request.results()
    results = []
    for observation in observations:
        # Return the string of the top VNRecognizedText instance.
        recognized_text = observation.topCandidates_(1)[0]
        results.append([recognized_text.string(), recognized_text.confidence()])
    for result in results:
        print(result)
    # TODO Process the recognized strings.

img_path = "pdf_images/page_1.png"

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
error = request_handler.performRequests_error_([request], None)