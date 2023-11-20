import rclpy
from rclpy.node import Node

from pause import milliseconds

from sensor_msgs.msg import JointState
from std_msgs.msg import UInt8MultiArray


# TODO fazer ser assignable, ou mudar para o escopo do projeto

#Objeto juntas dos motores:
class Joint:
    def __init__(self):
        self.lastPosition = 0.0
        self.firstIteration = True
        self.totalMoved = 0.0

#objeto convo:
class Convo(Node):
    
    def __init__(self):

        super().__init__("convo")
	
	#cria uma inscricao
        self.subscription = self.create_subscription(
            JointState, "joint_states", self.callback, 10
        )
        self.subscription

        # lista de objetos Joint TODO checar o número de joints disponíveis para criar do tamanho certo
        self.jointSelect = [Joint(), Joint(), Joint()]
        self.nJoints = 3

        # ligação com o serial_write do serial_bridge_node
        self.publisher_ = self.create_publisher(UInt8MultiArray, "serial_write", 10)

        # variável temporárias dentro do callback para formatação das mensagens
        self.string = ""

        # lista com FL/r para executar o comando
        self.feed = [70, 76, 13]

        # clock para uso da função sleep()
        self._loop_rate = self.create_rate(2, self.get_clock())
	
	#funcao retorno
    def callback(self, msg):
   	print("Debug\n\n\n\n\n")
        oMsg = UInt8MultiArray()
        
        for i in range(self.nJoints):
            #torna padrao os valores de posicao radial, variacao radial e variacao de passos:
            radPosition = msg.position[i]
            varRad = 0
            varSteps = 0
            
         	#verificacao de junta na posicao primaria e atualizacao de ultima posicao   
            if self.jointSelect[i].firstIteration:
                self.jointSelect[i].lastPosition = radPosition
                self.jointSelect[i].firstIteration = False
                
                #verifica se a posicao em rad e diferente da junta na ultima posicao:    
            elif radPosition != self.jointSelect[i].lastPosition:
            
            	#variacao radial = posicao radial-ultima posicao radial
                varRad = radPosition - self.jointSelect[i].lastPosition
                print(radPosition)
                print(self.jointSelect[i].lastPosition)
                
                #variacao de passos = valor inteiro da variacao / 0.0001745329
                varSteps = int(varRad / 0.0001745329)
                print(varRad)
                print(varSteps)
                
                #String de saida serial = posicao+comando+valor de passos->total movido da junta selecionada = somatorio variacao de passos
                string = str(1 + i) + "DI" + str(varSteps)
                self.jointSelect[i].totalMoved += varSteps
                print(self.jointSelect[i].totalMoved)
                
                self.get_logger().info("Comandos %s" % string + "FL")
                oMsg.data = [ord(c) for c in string] + [13]
                self.publisher_.publish(oMsg)
                milliseconds(10)
                string = ""
                self.jointSelect[i].lastPosition = radPosition
                if i == self.nJoints:
                    oMsg.data = self.feed
                    self.publisher_.publish(oMsg)
                    milliseconds(15)

    def inic(self):
        oMsg = UInt8MultiArray()

        string = "HR"
        oMsg.data = [ord(c) for c in string] + [13]
        string = "SK"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "MV"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "RLs"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "EG"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "IF"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "PR"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "PR5"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "PM"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "RV"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "SR-1"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "SV"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "SR100"
        oMsg.data += [ord(c) for c in string] + [13]
        string = "SV"
        oMsg.data += [ord(c) for c in string] + [13]

        oMsg.data = self.feed
        self.publisher_.publish(oMsg)

def main(args=None):
    rclpy.init(args=args)

    convo = Convo()

    rclpy.spin(convo)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    convo.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

