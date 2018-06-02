# people-counter
Count the number of people in a video based on facial recognition

## Installation
An anaconda environment file is provided. Follow the foloowing steps to easily install all dependencies.

1) Install anaconda [here](https://conda.io/docs/user-guide/install/index.html).
2) Create the tensorflow environment via YML file provided within the project directory.
    ```
    conda env create -f anaconda/environment.yml
    ```
3) Activate the environment
    ```
    # Ubuntu
    $ source activate tensorflow

    # Windows
    $ activate tensorflow
    ```

## Running the program
Follow the steps to run the code:
1) Place video file into `/data` folder.
2) Edit 'VIDEO_NAME' variable in ```run.py``` file.
3) Run the following command: 
    ```
    python run.py
    ```
4) Extract and place trained model files in ```/model`` folder. The files can be downloaded [here](https://mega.nz/#!BfglkI7A!YBvFyxgKhvUnnNRu9FL-ACjdo18SmOZ-YSz9QghQRzE). Or requested by emailing on rizasif@gmail.com. This model is required for age and gender recognition.


## Dependencies: 
Note: These are provided in the anaconda environment so no need to install 1&2 separately.
1) [face_recognition](https://github.com/ageitgey/face_recognition)
2) [Tensorflow](https://www.tensorflow.org/install/)
3) Trained model: The files can be downloaded [here](https://mega.nz/#!BfglkI7A!YBvFyxgKhvUnnNRu9FL-ACjdo18SmOZ-YSz9QghQRzE) or you can email me on rizasif@gmail.com to receive the trained model for age and gender recognition.
