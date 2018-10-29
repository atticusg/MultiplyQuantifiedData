import generate_data as gd
if __name__ == '__main__':
    train_size = 50#0000
    val_size = 10#000
    test_size = 10#000
    gd.create_corpus(train_size,"multiplyquantified.train")
    gd.create_corpus(val_size,"multiplyquantified.val")
    gd.create_corpus(test_size,"multiplyquantified.test")
