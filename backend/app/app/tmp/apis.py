ApiKey = "f023706e-ef2e-4340-bf9f-e61323fc319c"
ApiSecret = "416EF814C3D6354A3FBCD2DBA76D2ACD"
Passphrase = 'Sh528491@okx'

DemoApiKey = "28f036b8-baba-4f68-83c0-88d370605aa9"
DemoApiSecret = "12A756552CAFAF8F9267B0DEF219242A"
DemoPassphrase = 'Sh528491@okx'


from pedesis.components.contract.models import Position
import functools
class DemoPosition(Position):
    
    def get_broker(self):
        br = super().get_broker()
        br.set_sandbox_mode(True)
        return br
