# 功能
从pdf中orc中文

# install Tesseract & python libraries
1. **Install Tesseract OCR:**

   - **On Ubuntu:**
     You can use the following commands in the terminal:
     ```
     sudo apt update
     sudo apt install tesseract-ocr
     sudo apt install libtesseract-dev
     ```

   - **On macOS:**
     If you have Homebrew installed, you can use the following command in the terminal:
     ```
     brew install tesseract
     ```

2. **Install the Chinese language data for Tesseract:**

   - **On Ubuntu:**
     You can use the following command in the terminal:
     ```
     sudo apt-get install tesseract-ocr-chi-sim
     ```

   - **On macOS:**
     You can use the following command in the terminal:
     ```
     brew install tesseract-lang
     ```

3. **Install the necessary Python libraries:**

   You will need the following libraries: PyTesseract, pdf2image, and Pillow. You can install them using pip:

   ```
   pip install pytesseract pdf2image pillow
   ```

   Please note that `pdf2image` requires `poppler-utils` to be installed on your machine. To install `poppler-utils`, you can use the following commands:

   - **On Ubuntu:**
     ```
     sudo apt-get install -y poppler-utils
     ```

   - **On macOS:**
     ```
     brew install poppler
     ```

   - **On Windows:**
     You can download the binary from [this page](http://blog.alivate.com.au/poppler-windows/) and add the `bin/` folder to your PATH.
