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

> Once you've done that open a new terminal for the frontend local host

cd frontend
npm install
npm run dev

### Usage

Steam searches intention is to provide a quick simple look up of some of the games across steam, and in doing so compare the trie and heap data structures.
