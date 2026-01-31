from dotenv import load_dotenv


def main() -> int:
    load_dotenv()
    from src.interface_adapter.controllers.ngrok_tunnel_controller import NgrokTunnelController

    return NgrokTunnelController().run()


if __name__ == "__main__":
    raise SystemExit(main())
