# KiwqSense

## Overview

KiwqSense is an AI-powered system designed to enhance public safety by analyzing visual data for potential threats. Utilizing advanced models such as NVIDIA's LLaMA (Large Language Model Meta AI), KiwqSense aims to address the pressing issue of crime against women in public spaces. This innovative solution leverages the power of computer vision and natural language processing to provide real-time analysis and alerts.

## Problem Statement

Our country needs to make public spaces safer. Can an AI-powered system solve for reducing the rate of crimes against women? KiwqSense endeavors to answer this question by providing a proactive approach to threat detection and safety assessment.

## Features

- **Image Analysis**: KiwqSense utilizes NVIDIA's LLaMA vision model to analyze images and detect potential threats in real-time.
- **Telegram Alerts**: When a dangerous situation is detected, KiwqSense automatically sends alerts via Telegram, including relevant details and visual evidence.
- **User-Friendly Interface**: The system is designed for easy interaction, allowing users to upload images for analysis and receive instant feedback.

## Installation

### Prerequisites

- Python 3.7 or later
- FastAPI
- Required libraries:
  - `requests`
  - `pydantic`
  - `dotenv`
  - `cachetools`
  - `langchain`
  
You can install the required libraries using pip:

```bash
pip install fastapi requests pydantic python-dotenv cachetools langchain
```

### Setting Up Environment Variables

Create a `.env` file in the root directory of the project with the following variables:

```plaintext
API_KEY=<Your_NVIDIA_API_Key>
TELEGRAM_BOT_TOKEN=<Your_Telegram_Bot_Token>
CHANNEL_ID=<Your_Telegram_Channel_ID>
```

## Usage

1. **Start the FastAPI server**:

   Run the following command in your terminal:

   ```bash
   uvicorn main:app --reload
   ```

2. **Upload an image for threat analysis**:

   Use the `/detect-threat/` endpoint to upload an image. The server will analyze the image and respond with the threat level and any relevant descriptions.

   Example using `curl`:

   ```bash
   curl -X POST "http://127.0.0.1:8000/detect-threat/" -F "file=@path_to_your_image.jpg"
   ```

3. **Receive Alerts**:

   If a threat is detected, KiwqSense will send a notification to your specified Telegram channel, including the image and a description of the threat.

## How It Works

1. **Image Upload**: Users upload images to the FastAPI application.
2. **Threat Analysis**: The image is encoded and sent to the NVIDIA LLaMA vision model for analysis.
3. **Response Handling**: Based on the analysis, KiwqSense determines if a threat exists and responds accordingly.
4. **Alerting**: If a dangerous situation is detected, an alert is sent via Telegram with the relevant details.

## Contributing

We welcome contributions to enhance KiwqSense. Please fork the repository and submit a pull request with your improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- NVIDIA for the LLaMA model and its powerful capabilities.
- FastAPI for providing a robust framework for building APIs.
- The open-source community for their continuous support and contributions.



