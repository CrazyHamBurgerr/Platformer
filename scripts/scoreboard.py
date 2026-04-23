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
        for i in self.__score:
            print(f"{i:2}", f"{self.__score[str(i)]['score']: 5d}", datetime.datetime.fromtimestamp(self.__score[str(i)]['timestamp']))

    def new_entry(self, new_score, timestamp):
        self.__score[str(len(self.__score)+1)] = {"score": new_score, "timestamp": timestamp}

    def save(self):
        self.sort()
        file = open('score.json', 'w')
        json.dump({'score': self.__score}, file)
        file.close()

    def sort(self):
        temp_list = []
        for i in self.__score:
            temp_list.append(self.__score[str(i)])
        
        self.__score.clear()

        temp_list = sorted(temp_list, key=lambda dict: dict['score'], reverse = True)
        for i in range(len(temp_list)):
            self.__score[str(i+1)] = temp_list[i]
        del temp_list
    
    def delete_entry(self, position):
        try:
            position = int(position)
            if position > 0 and position < len(self.__score) + 1:
                del self.__score[str(position)]
                print(f"entry {position} deleted")
            else:
                print("input position is not positive or too large")
        except:
            print(f"incorrect input, correct input is an interger between 1 and {len(self.__score)+1}")