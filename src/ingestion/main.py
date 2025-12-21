import sys
import os

# Add the src directory to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.ingestion.producer import UserActivityProducer

def main():
    try:
        print("Initializing Producer...")
        producer = UserActivityProducer()
        
        while True:
            try:
                count = int(input("Enter number of events to produce (0 to exit): "))
                if count == 0:
                    break
                producer.produce_events(count=count, delay=0.2)
            except ValueError:
                print("Please enter a valid number.")
                
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    main()
