import modal

def main():
    try:
        Pricer = modal.Cls.from_name("pricer-service", "Pricer")
        pricer = Pricer()
        # Try to call the wake_up method which should be lightweight
        result = pricer.wake_up.remote()
        print(f"Service responded with: {result}")
    except Exception as e:
        print(f"Error connecting to Modal service: {str(e)}")

if __name__ == "__main__":
    main() 