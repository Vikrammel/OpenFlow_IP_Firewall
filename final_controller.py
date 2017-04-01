# Final Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.

    #ofp_flow_mod() var and properties
    flowMsg = of.ofp_flow_mod()
    flowMsg.idle_timeout = 60
    flowMsg.hard_timeout = 60
    flowMsg.match = of.ofp_match.from_packet(packet)
    flowMsg.data = packet_in

    #packet type Boolean vars
    ip = packet.find('ipv4')
    icmp = packet.find('icmp')

    # print packet
    if ip is None: #if non-ip packet	
    	msgAction = of.ofp_action_output(port = of.OFPP_FLOOD)
    	flowMsg.actions.append(msgAction)
    	#print 'non-ip, flooded'

    else: #packet is ip packet
    	if switch_id is 1:
    		#print 'ip at s1'
    		if port_on_switch is 1: #from h1
    			msgAction = of.ofp_action_output(port = 2) #send to s4
    			flowMsg.actions.append(msgAction)
    			#print 'sent to s4'
    		elif port_on_switch is 2: #from s4
    			msgAction = of.ofp_action_output(port = 1) #send to h1
    			flowMsg.actions.append(msgAction)
    			#print 'sent to h1'

    	elif switch_id is 2:
    		#print 'ip at s2'
    		if port_on_switch is 1: #from h2
    			msgAction = of.ofp_action_output(port = 2) #send to s4
    			flowMsg.actions.append(msgAction)
    			#print 'sent to s4'
    		elif port_on_switch is 2: #from s4
    			msgAction = of.ofp_action_output(port = 1) #send to h2
    			flowMsg.actions.append(msgAction)
    			#print 'sent to h2'

    	elif switch_id is 3:
    		#print 'ip at s3'
    		if port_on_switch is 1: #from h3
    			msgAction = of.ofp_action_output(port = 2) #send to s4
    			flowMsg.actions.append(msgAction)
    			#print 'sent to s4'
    		elif port_on_switch is 2: #from s4
    			msgAction = of.ofp_action_output(port = 1) #send to h3
    			flowMsg.actions.append(msgAction)
    			#print 'sent to h3'

    	elif switch_id is 5:
    		#print 'ip at s5'
    		if port_on_switch is 1: #from h5
    			msgAction = of.ofp_action_output(port = 2) #send to s4
    			flowMsg.actions.append(msgAction)
    			#print 'sent to s4'
    		elif port_on_switch is 2: #from s4
    			msgAction = of.ofp_action_output(port = 1) #send to h5
    			flowMsg.actions.append(msgAction)
    			#print 'sent to h5'
    	elif switch_id is 4:
    		#print 'ip at s4'
    		if port_on_switch is 1: 
    			#from untrusted host h4 to server h5, drop
    			if icmp is not None:
    				self.connection.send(flowMsg)
    				#print 'icmp packet from h4 dropped'
    				return
    			elif ip.dstip == '10.5.5.50': #drop ip packet to h5 from h4
    				self.connection.send(flowMsg)
    				#print 'ip packet from h4 to h5 dropped'
    				return
    			elif ip.dstip == '10.1.1.10': #forward to h1
    				msgAction = of.ofp_action_output(port = 2)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 1'
    			elif ip.dstip == '10.2.2.20': #forward to h2
    				msgAction = of.ofp_action_output(port = 3)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 2'
    			elif ip.dstip == '10.3.3.30': #forward to h3
    				msgAction = of.ofp_action_output(port = 4)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 3'

    		else:
    			if ip.dstip == '123.45.67.89': #forward to h4
    				msgAction = of.ofp_action_output(port = 1)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 4'
    			elif ip.dstip == '10.1.1.10': #forward to h1
    				msgAction = of.ofp_action_output(port = 2)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 1'
    			elif ip.dstip == '10.2.2.20': #forward to h2
    				msgAction = of.ofp_action_output(port = 3)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 2'
    			elif ip.dstip == '10.3.3.30': #forward to h3
    				msgAction = of.ofp_action_output(port = 4)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 3'
    			elif ip.dstip == '10.5.5.50': #forward to h5
    				msgAction = of.ofp_action_output(port = 5)
    				flowMsg.actions.append(msgAction)
    				#print 'sent o host 5'

    self.connection.send(flowMsg)
    return

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
