import json
import datetime
import time

class ScoreBoard:
    instance = None

    def __new__(cls, name):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self, name):
        self.__score = {}
        try:
            file = open(name, 'r')
            score_data = json.load(file)
            file.close()
            self.__score = score_data['score']
        except FileNotFoundError:
            pass
        
    def print(self):
        for i in self.__score:
            print(f"{i:2}", f"{self.__score[str(i)]['score']: 5d}", 
                  datetime.datetime.fromtimestamp(self.__score[str(i)]['timestamp']))

    def new_entry(self, new_score, timestamp):
        try:
            if abs(time.time() - timestamp) < 600:
                try:
                    new_score = int(new_score)
                    if new_score < 0 or new_score > 6000:
                        return "invalid score"
                    self.sort()
                    self.__score[str(len(self.__score)+1)] = {"score": new_score, "timestamp": timestamp}
                    return True
                except:
                    return "invalid score type"
            else:
                return "bad timestamp"
        except:
            return "bad timestamp"
    
    def return_entry(self, position):
        if self.check_valid_position(position):
            return self.__score[str(position)]
        
    def delete_entry(self, position):
        if self.check_valid_position(position):
            del self.__score[str(position)]
            self.sort()
            return f"entry {position} deleted"

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

    def check_valid_position(self, position):
        try:
            position = int(position)
            for i in self.__score:
                if str(position) == i:
                    return True
            else:
                print("input position is incorrect")
                return False
        except TypeError:
            print("incorrect input type")
            return False
        
mock_score = ScoreBoard('mockscore.json')
print(mock_score.return_entry(5))
mock_score.new_entry(5600, time.time())
mock_score.print()