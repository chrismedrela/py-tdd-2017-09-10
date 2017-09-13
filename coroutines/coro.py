def receive():
    while True:
        packet_type, packet_data = next_packet()
        if packet_type == 'PING':
            send_to_client(
                "PONG", packet_data)
        elif packet_type == 'MESSAGE':
            response = trigger_event(
                'message', packet_data)
            send_to_client('MESSAGE', response)
        else:
            raise ValueError('Invalid packet type')

def next_packet():
    return ('PING', 'data')

def send_to_client(packet_type, packet_data):
    print('send_to_client', packet_type, packet_data)

def trigger_event(event_name, event_data):
    print('trigger_event', event_name, event_data)