# Public Safety AI System

## Overview

Our country needs to make public spaces safer. Can an AI-powered system, specifically leveraging the NVIDIA LLaMA Vision Model, effectively reduce the rate of crimes against women? This application utilizes advanced image analysis capabilities to identify potential threats in public areas and notify authorities through Telegram alerts.

## Features

- **Image Analysis**: Uses the NVIDIA LLaMA Vision model to assess images for potential threats to public safety.
- **Real-time Alerts**: Sends alerts to a specified Telegram channel with details and images when a dangerous situation is detected.
- **Caching**: Implements a caching mechanism to optimize performance and avoid duplicate analyses.
- **Environment Configuration**: Utilizes environment variables for sensitive data management.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `pip` for installing packages

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/public-safety-ai.git
   cd public-safety-ai
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables. Create a `.env` file in the root directory of your project with the following content:
   ```
   API_KEY=your_nvidia_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   CHANNEL_ID=your_telegram_channel_id
   ```

### Usage

1. **Run the FastAPI server**:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```

2. **Test the Telegram connection**:
   Once the server is running, the console will indicate whether the Telegram setup is working correctly.

3. **Send a request to analyze an image**:
   You can use a tool like `curl`, Postman, or any HTTP client to test the endpoint. Here’s an example using `curl`:
   ```bash
   curl -X POST "http://127.0.0.1:8000/detect-threat/" -F "file=@path_to_your_image.jpg"
   ```

### Endpoints

- **POST /detect-threat/**: Analyzes the uploaded image for potential threats and sends alerts if necessary.

### Response Format

- When a dangerous situation is detected:
  ```json
  {
      "alert": "dangerous",
      "description": "Detailed description of the threat.",
      "telegram_alert_sent": true
  }
  ```

- When no threat is detected:
  ```json
  {
      "alert": "not dangerous"
  }
  ```

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **NVIDIA**: For providing the LLaMA Vision model which powers the threat detection capabilities.
- **FastAPI**: For the fast and efficient framework used to build this application.

