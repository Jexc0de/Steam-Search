### Name: Steam Search

### Description

Steam Search uses a dataset of roughly 130,000 Games all from the steam website along with search to provide the simpilest and fastest look up of some of your favorite games!

### Installation

Once you've downloaded the repo and are in the directory, do the following commands for windows or their linux/mac equal

cd backend

python -m venv venv

(then activate the virutal enviroment for the backend)
venv\Scripts\activate

pip install -r requirements.txt

python app.py

> (make sure the local host the server is running on is the same that the fetchs are being sent too on Frontend\src\MainPage.jsx lines 13 and 21, by default its port 5000)

> Once you've done, open a new terminal for the frontend local host

cd frontend
npm install
npm run dev

### Usage

[Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.]

### Authors and acknowledgment

[Anyone who have contributed to the project.]

### Project status

In development.
