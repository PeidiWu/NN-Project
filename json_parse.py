import ijson
import datetime

# Convert 2 digit hex chains to int
def hex_bytes_to_int(offset, length):
    hex_string = []
    for payload_offset in range(offset, offset + length):
        hex_string.append(value[payload_offset * 3 : payload_offset * 3 + 2])
    hex_string = ''.join(reversed(hex_string))
    int_value = int(hex_string, 16)
    return int_value

# Convert 2 digit hex chains to str
def hex_bytes_to_str(offset, length):
    hex_string = []
    for payload_offset in range(offset, offset + length):
        hex_string.append(value[payload_offset * 3 : payload_offset * 3 + 2])
    hex_string = ''.join(reversed(hex_string))
    str_value = bytearray.fromhex(hex_string).decode()
    return str_value

# Parse out the historical data
# m_s,m_d,m_h,m_o,m_p,m_e,m_8,m_5,m_t,m_x,m_b,m_a,m_na = (0,0,0,0,0,0,0,0,0,0,0,0,0) # For testing so each message type only appears once
with open('/NN/Historical Data/IEX/IEX HIST/IEX_DEEP_20170515.json') as f:
    parser = ijson.parse(f)
    packet_num = 1
    for prefix, event, value in parser:
        if prefix.endswith('data.data'):
            
            msg_ct = hex_bytes_to_int(14,2) # check if message exists, otherwise skip

            # For testing so each message type only appears once
            # if (m_s==1) or (m_d==1) or (m_h==1) or (m_o==1) or (m_p==1) or (m_e==1) or (m_8==1) or (m_5==1) or (m_t==1) or (m_x==1) or (m_b==1) or (m_a==1) or (m_na==1):
            #     continue

            if msg_ct > 0:
                print('\nPacket Number: %s -------------------------------------------------------------------------------------------------' % packet_num)
                packet_num += 1
                if packet_num == 999:
                    break
                print('Payload in Hex: %s' % value)        

                htimestamp_int = hex_bytes_to_int(32,8)/1000000000            
                htimestamp_utc = datetime.datetime.utcfromtimestamp(htimestamp_int).strftime('%Y-%m-%d %H:%M:%S.%f')
                print('Header Timestamp: %s' % htimestamp_utc)

                # print('Message Count: %s' % msg_ct)

                # pl_l = hex_bytes_to_int(12,2)
                # print('Payload Length: %s' % pl_l)
            
                # Print out each message
                msg_len = 0
                msg_len_t = 0
                for msg_num in range(1, msg_ct + 1):

                    msg_len = hex_bytes_to_int(40 + msg_len_t, 2)
                    print('\nStart of Message %s (length = %s)' % (msg_num, msg_len))

                    msg_type_c = hex_bytes_to_str(40 + msg_len_t + 2, 1)

                    if msg_type_c == 'S': # System Event Msg
                        # m_s=1
                        print('Message Type: System Event Message')

                        if hex_bytes_to_str(40 + msg_len_t + 3, 1) == 'O':
                            print('Start of Day Message')
                        elif hex_bytes_to_str(40 + msg_len_t + 3, 1) == 'S':
                            print('Start of System Hours')
                        elif hex_bytes_to_str(40 + msg_len_t + 3, 1) == 'R':
                            print('Start of Regular Market Hours')
                        elif hex_bytes_to_str(40 + msg_len_t + 3, 1) == 'M':
                            print('End of Regular Market Hours')                            
                        elif hex_bytes_to_str(40 + msg_len_t + 3, 1) == 'E':
                            print('End of System Hours')
                        elif hex_bytes_to_str(40 + msg_len_t + 3, 1) == 'C':
                            print('End of Day Message')

                        htimestamp_int = hex_bytes_to_int(40 + msg_len_t + 4, 8)/1000000000            
                        htimestamp_utc = datetime.datetime.utcfromtimestamp(htimestamp_int).strftime('%Y-%m-%d %H:%M:%S.%f')
                        print('Timestamp: %s' % htimestamp_utc)

                    elif msg_type_c == 'D': # Security Directory Message
                        # m_d=1
                        print('Message Type: Security Directory Message')
                        
                        flag = hex_bytes_to_str(40 + msg_len_t + 3, 1)

                    elif msg_type_c == 'H': # Trading Status Message
                        # m_h=1
                        print('Message Type: Trading Status Message')

                        trading_status = hex_bytes_to_str(40 + msg_len_t + 3, 1)
                        if trading_status == 'T':
                            print('Trading Status: Trading')

                            htimestamp_int = hex_bytes_to_int(40 + msg_len_t + 4, 8)/1000000000            
                            htimestamp_utc = datetime.datetime.utcfromtimestamp(htimestamp_int).strftime('%Y-%m-%d %H:%M:%S.%f')
                            print('Timestamp: %s' % htimestamp_utc)

                            symbol = hex_bytes_to_str(40 + msg_len_t + 12, 8).strip()
                            print('Symbol: %s' % symbol)

                        elif trading_status == 'H':
                            print('Trading Status: Halted accross all US equity markets')

                            htimestamp_int = hex_bytes_to_int(40 + msg_len_t + 4, 8)/1000000000            
                            htimestamp_utc = datetime.datetime.utcfromtimestamp(htimestamp_int).strftime('%Y-%m-%d %H:%M:%S.%f')
                            print('Timestamp: %s' % htimestamp_utc)

                            symbol = hex_bytes_to_str(40 + msg_len_t + 12, 8).strip()
                            print('Symbol: %s' % symbol)

                            reason = hex_bytes_to_str(40 + msg_len_t + 20, 8)
                            print('Reason: %s' % reason)

                        elif trading_status == 'O':
                            print('Trading Status: Halted, released into an order acceptance period')

                            htimestamp_int = hex_bytes_to_int(40 + msg_len_t + 4, 8)/1000000000            
                            htimestamp_utc = datetime.datetime.utcfromtimestamp(htimestamp_int).strftime('%Y-%m-%d %H:%M:%S.%f')
                            print('Timestamp: %s' % htimestamp_utc)

                            symbol = hex_bytes_to_str(40 + msg_len_t + 12, 8).strip()
                            print('Symbol: %s' % symbol)

                            reason = hex_bytes_to_str(40 + msg_len_t + 20, 8)
                            print('Reason: %s' % reason)

                        elif trading_status == 'P':
                            print('Trading Status: Paused')

                            htimestamp_int = hex_bytes_to_int(40 + msg_len_t + 4, 8)/1000000000            
                            htimestamp_utc = datetime.datetime.utcfromtimestamp(htimestamp_int).strftime('%Y-%m-%d %H:%M:%S.%f')
                            print('Timestamp: %s' % htimestamp_utc)

                            symbol = hex_bytes_to_str(40 + msg_len_t + 12, 8).strip()
                            print('Symbol: %s' % symbol)
                        
                    elif msg_type_c == 'O': # Operational Halt Status Message
                        # m_o=1
                        print('Message Type: Operational Halt Status Message')

                        halt_status = hex_bytes_to_str(40 + msg_len_t + 3, 1)
                        print('Operational Halt Status: %s' % halt_status)

                        htimestamp_int = hex_bytes_to_int(40 + msg_len_t + 4, 8)/1000000000            
                        htimestamp_utc = datetime.datetime.utcfromtimestamp(htimestamp_int).strftime('%Y-%m-%d %H:%M:%S.%f')
                        print('Timestamp: %s' % htimestamp_utc)

                        symbol = hex_bytes_to_str(40 + msg_len_t + 12, 8).strip()
                        print('Symbol: %s' % symbol)

                    elif msg_type_c == 'P': # Short Sale Price Test Status Message
                        # m_p=1
                        print('Message Type: Short Sale Price Test Status Message')

                        sspt_status = value[(40 + msg_len_t + 3) * 3 + 1 : (40 + msg_len_t + 3) * 3 + 2]
                        if int(sspt_status) == 0:
                            print('Short Sale Price Test Status: Not restricted from short sale')
                        elif int(sspt_status) == 1:
                            print('Short Sale Price Test Status: Restricted from short sale')

                        htimestamp_int = hex_bytes_to_int(40 + msg_len_t + 4, 8)/1000000000            
                        htimestamp_utc = datetime.datetime.utcfromtimestamp(htimestamp_int).strftime('%Y-%m-%d %H:%M:%S.%f')
                        print('Timestamp: %s' % htimestamp_utc)

                        symbol = hex_bytes_to_str(40 + msg_len_t + 12, 8).strip()
                        print('Symbol: %s' % symbol)

                    elif msg_type_c == 'E': # Security Event Message
                        # m_e=1
                        print('Message Type: Security Event Message')

                    elif msg_type_c == '8': # Price Level Update on Buy Side Message
                        # m_8=1
                        print('Message Type: Price Level Update on Buy Side Message')

                        flag = value[(40 + msg_len_t + 3) * 3 + 1 : (40 + msg_len_t + 3) * 3 + 2]
                        if flag == 1:
                            print('Order Book transition complete')
                        elif flag == 0:
                            print('Order Book is in transition')

                        htimestamp_int = hex_bytes_to_int(40 + msg_len_t + 4, 8)/1000000000            
                        htimestamp_utc = datetime.datetime.utcfromtimestamp(htimestamp_int).strftime('%Y-%m-%d %H:%M:%S.%f')
                        print('Timestamp: %s' % htimestamp_utc)

                        symbol = hex_bytes_to_str(40 + msg_len_t + 12, 8).strip()
                        print('Symbol: %s' % symbol)

                        size = hex_bytes_to_int(40 + msg_len_t + 20, 4)
                        print('Size: %s' % size)

                        price = float(hex_bytes_to_int(40 + msg_len_t + 24, 8)/1000)
                        print('Price: %s' % price)

                    elif msg_type_c == '5': # Price Level Update on Sell Side Message
                        # m_5=1
                        print('Message Type: Price Level Update on Sell Side Message')

                        flag = value[(40 + msg_len_t + 3) * 3 + 1 : (40 + msg_len_t + 3) * 3 + 2]
                        if flag == 1:
                            print('Order Book transition complete')
                        elif flag == 0:
                            print('Order Book is in transition')

                        htimestamp_int = hex_bytes_to_int(40 + msg_len_t + 4, 8)/1000000000            
                        htimestamp_utc = datetime.datetime.utcfromtimestamp(htimestamp_int).strftime('%Y-%m-%d %H:%M:%S.%f')
                        print('Timestamp: %s' % htimestamp_utc)

                        symbol = hex_bytes_to_str(40 + msg_len_t + 12, 8).strip()
                        print('Symbol: %s' % symbol)

                        size = hex_bytes_to_int(40 + msg_len_t + 20, 4)
                        print('Size: %s' % size)

                        price = float(hex_bytes_to_int(40 + msg_len_t + 24, 8)/1000)
                        print('Price: %s' % price)

                    elif msg_type_c == 'T': # Trade Report Message
                        # m_t=1
                        print('Message Type: Trade Report Message')

                        sale_condition_flag = value[(40 + msg_len_t + 3) * 3 + 0 : (40 + msg_len_t + 3) * 3 + 1]
                        flag = value[(40 + msg_len_t + 3) * 3 + 1 : (40 + msg_len_t + 3) * 3 + 2]
                        if sale_condition_flag == '7':
                            print('Intermarket Sweep Flag: %s' % flag)
                        elif sale_condition_flag == '6':
                            print('Extended Hours Flag: %s' % flag)
                        elif sale_condition_flag == '5':
                            print('Odd Lot Flag: %s' % flag)
                        elif sale_condition_flag == '4':
                            print('Trade Through Exempt Flag: %s' % flag)
                        elif sale_condition_flag == '3':
                            print('Single-price Cross Trade Flag: %s' % flag)

                        htimestamp_int = hex_bytes_to_int(40 + msg_len_t + 4, 8)/1000000000            
                        htimestamp_utc = datetime.datetime.utcfromtimestamp(htimestamp_int).strftime('%Y-%m-%d %H:%M:%S.%f')
                        print('Timestamp: %s' % htimestamp_utc)

                        symbol = hex_bytes_to_str(40 + msg_len_t + 12, 8).strip()
                        print('Symbol: %s' % symbol)

                        size = hex_bytes_to_int(40 + msg_len_t + 20, 4)
                        print('Size: %s' % size)

                        price = float(hex_bytes_to_int(40 + msg_len_t + 24, 8)/1000)
                        print('Price: %s' % price)

                        trade_id = hex_bytes_to_int(40 + msg_len_t + 32, 8)
                        print('Trade ID: %s' % trade_id)

                    elif msg_type_c == 'X': # Official Price Message
                        # m_x=1
                        print('Message Type: Official Price Message')

                    elif msg_type_c == 'B': # Trade Break Message
                        # m_b=1
                        print('Message Type: Trade Break Message')
                        
                    elif msg_type_c == 'A': # Auction Information Message
                        # m_a=1
                        print('Message Type: Auction Information Message')

                    else:
                        # m_na=1
                        print('Message Type Not in Dictionary. Please Update Code.')
                        
                    msg_num += 1
                    msg_len_t = msg_len_t + msg_len + 2





                    

            



                
