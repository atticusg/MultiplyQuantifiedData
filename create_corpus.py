import generate_data as gd
import random
if __name__ == '__main__':
    train_size = 500000
    val_size = 10000
    test_size = 10000
    data, _, _ = gd.process_data(1.0)
    examples = gd.generate_balanced_data("simple_solutions", "boolean_solutions", train_size, 0, data, simple_sampling = "level 2", boolean_sampling = "level 0")
    gd.save_data(examples, "multiplyquantified.train")
    examples = gd.generate_balanced_data("simple_solutions", "boolean_solutions", val_size, 0, data, simple_sampling = "level 2", boolean_sampling = "level 0")
    gd.save_data(examples, "multiplyquantified.val")
    examples = gd.generate_balanced_data("simple_solutions", "boolean_solutions", test_size, 0, data, simple_sampling = "level 2", boolean_sampling = "level 0")
    gd.save_data(examples, "multiplyquantified.test")
