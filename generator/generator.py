# artificial time series -> kafka
import argparse

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch-size', dest='batch_size', type=int)
    # whether the data should be constantly streamed to kafka (while True: publish)
    parser.add_argument('--stream', dest='stream', type=bool)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    print(args)
    if args.repeat:
        while True:
            pass
    else:
        pass