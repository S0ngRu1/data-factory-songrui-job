from abc import ABC, abstractmethod

class TrainDataGeneraterABC(ABC):
    
    @abstractmethod
    def lbl_std2train_data(self):
        pass

    @abstractmethod
    def train_data2lbl_std(self):
        pass

    @abstractmethod
    def predict_data2lbl_std(self):
        pass
    
    @abstractmethod
    def split_train_val_datasets(self):
        pass