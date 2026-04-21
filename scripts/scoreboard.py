import json
import datetime

class ScoreBoard:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.__score = {}
        try:
            file = open('score.json', 'r')
            score_data = json.load(file)
            file.close()
            self.__score = score_data['score']
        except FileNotFoundError:
            pass
        
    def print(self):
        for i in range(len(self.__score)):
            print(i+1, self.__score[str(i+1)]['score'], datetime.datetime.fromtimestamp(self.__score[str(i+1)]['timestamp']))

    def new_entry(self, new_score, timestamp):
        self.__score[str(len(self.__score)+1)] = {"score": new_score, "timestamp": timestamp}

    def save(self):
        file = open('score.json', 'w')
        json.dump({'score': self.__score}, file)
        file.close()