from nicegui import ui, app, Tailwind, events
import os
from pythonping import ping




######################## Variables #########################################
##PAGINAS
pag_main = '/'
pag_cdp = '/cdp'
pag_new = '/new'
pag_tracepath = '/tracepath'

##STATIC
app.add_static_files('/nextui-cdp', 'NextUI-CDP')
app.add_static_files('/sample', 'NextUI-sample')
app.add_static_files('/imgs', 'imgs')
app.add_static_files('/passw', 'inventory')


pag_CDP = """
<iframe src="/nextui-cdp/index.html" width="530%" height="800" style="border:1px solid black;">
</iframe>
"""

pag_example = """
<iframe src="/sample/index.html" width="530%" height="800"     style="border:1px solid black;">
</iframe>
"""
html_head = """
<p><img src="https://drive.google.com/uc?export=view&amp;id=1sX1P9gywMQPFhSjHJGyaosAdOJm1lfSl" alt="JID-OEA" width="741" height="168" /></p>
<table border="0" style="height: 21px; width: 100%; border-collapse: collapse; border-style: hidden;">
<tbody>
<tr style="height: 21px;">
<td style="width-: 33.3333%; height: 21px;"></td>
<td style="width: 33.3333%; height: 21px; text-align: center;"><span style="text-decoration: underline;"><strong>Estadistica de Seminarios</strong></span></td>
<td style="width: 33.3333%; height: 21px;"></td>
</tr>
</tbody>
</table>
"""
rPing = ''

######################## Pagina MAIN #########################################

def save_file(information):
    with open('NextUI-sample/topology.js', 'w', newline='') as file:
        file.write(information)
    app.add_static_files('/sample', 'NextUI-sample')
    
ui.label('Ctrl + F5 to reload cache').classes(' text-h6 font-semibold') 

ui.html(pag_example)
ui.label('Upload or download a topology for visualization in JS format (Ctrl + F5 to reload cache)').classes(' text-h6 font-semibold') 
with ui.row():
    ui.upload(on_upload=lambda e: save_file(e.content.read().decode('utf-8')), auto_upload=True , label='Upload topology.js')
    ui.button('Download topology', on_click=lambda: ui.download('/sample/topology.js'))    


## Encabezado    
with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
    with ui.row().style('background-color: #3874c8'):
        with ui.button(on_click=lambda: menu.open()).props('icon=menu'):
            with ui.menu() as menu:
                ui.menu_item('Inicio', lambda: ui.open(pag_main), auto_close=True)
                ui.menu_item('Diagrama por CDP', lambda: ui.open(pag_cdp), auto_close=True)
                ui.menu_item('Gráfica L2 (Trace Path)',lambda: ui.open(pag_tracepath), auto_close=True)
                ui.separator()                
                ui.menu_item('Close', on_click=menu.close)
        ui.label(' . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . ').tailwind('drop-shadow', 'font-bold', 'text-blue-500')
        ui.label('  Sistema de Moniteo, Control y Recuperacion ').classes(' text-h5 font-semibold') 
        ui.label(' . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . ').tailwind('drop-shadow', 'font-bold', 'text-blue-500')
        ui.html('<img src="imgs/Escudo OEA.png" alt="JID-OEA" width="60px" />')
        ui.html('<img src="imgs/Escudo JID.png" alt="JID-OEA" width="60px" height="68"/>')

with ui.footer().style('background-color: #3874c8'):
    ui.html('Más información: <strong> https://github.com/joserev')
    


######################## Pagina CDP #########################################
#async def pong(r_ping):
 #   texto=ping("127.0.0.1", verbose=True)   
  #  print('uno -',texto)
   # r_ping.set_text(str(texto))
    #return str(texto)                

@ui.page(pag_cdp)
async def pag_cdp():

    def save_passw(information):
        with open('inventory/hosts.yaml', 'w', newline='') as file:
            file.write(information)
    with ui.row():
        ui.label(' . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ').style('color: #ffffff')
        ui.button('Start discovery', on_click=lambda: os.system('python "nornir - cdp.py"'), color='green')        
    ui.label('Ctrl + F5 to reload cache').classes(' text-h6 font-semibold') 
    ui.html(pag_CDP)
    ui.label('- Upload or download the inventory for CDP discovery (YAML)').classes(' text-h6 font-semibold') 
    ui.label('- Download topology in (JS)').classes(' text-h6 font-semibold') 
    ui.label('- Ctrl + F5 to reload cache').classes(' text-h6 font-semibold') 

    with ui.row():
        ui.upload(on_upload=lambda e: save_passw(e.content.read().decode('utf-8')), auto_upload=True , label='Upload inventory')
        ui.button('Download inventory (YAML)', on_click=lambda: ui.download('/passw/hosts.yaml')) #dialog.open() )    
        ui.button('Download topology (JS)', on_click=lambda: ui.download('/nextui-cdp/topology.js'))    
    #with ui.row().classes('w-full items-center'):
        
    
    
    ## Encabezado    
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        with ui.row().style('background-color: #3874c8'):
            with ui.button(on_click=lambda: menu.open()).props('icon=menu'):
                with ui.menu() as menu:
                    ui.menu_item('Inicio', lambda: ui.open(pag_main), auto_close=True)
                    ui.menu_item('Diagrama por CDP', lambda: ui.open(pag_cdp), auto_close=True)
                    ui.menu_item('Gráfica L2 (Trace Path)',lambda: ui.open(pag_tracepath), auto_close=True)
                    ui.separator()                
                    ui.menu_item('Close', on_click=menu.close)
            ui.label(' . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . ').tailwind('drop-shadow', 'font-bold', 'text-blue-500')
            ui.label('  Sistema de Moniteo, Control y Recuperacion ').classes(' text-h5 font-semibold') 
            ui.label(' . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . ').tailwind('drop-shadow', 'font-bold', 'text-blue-500')
            ui.html('<img src="imgs/Escudo OEA.png" alt="JID-OEA" width="60px" />')
            ui.html('<img src="imgs/Escudo JID.png" alt="JID-OEA" width="60px" height="68"/>')            

    with ui.footer().style('background-color: #3874c8'):
        ui.html('Más información: <strong> https://github.com/joserev')

    #def ping(address):
        #text = ping('127.0.0.1', verbose=True)
        #return text

    with ui.dialog() as dialog, ui.card():
        ui.label('Hello world!')
        ui.button('Close', on_click=dialog.close)

        
    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
        ui.label(' . ').style('color: #ebf1fa')
        ui.label(' . ').style('color: #ebf1fa')
        ui.label(' . ').style('color: #ebf1fa')
        ui.label(' . ').style('color: #ebf1fa')
        ui.label('Ping:').classes('text-center text-h6 font-semibold') 
        ui.label(' . ').style('color: #ebf1fa')
        ip_cdp = ui.input(label='IP', placeholder='start typing')
        
        ui.label(' . ').style('color: #ebf1fa')

        with ui.row():            
            ui.label(' . . . . . . . . . . .').style('color: #ebf1fa')
            ui.button('Start', on_click=  lambda: a.set_text(ping_(ip_cdp.value)))    
        ui.label(' . ').style('color: #ebf1fa')
        a= ui.label(rPing)
######################## Pagina Tracepath #########################################
@ui.page(pag_tracepath)
async def pag_tracepath():
    ui.label('Trace Path').classes('w-full text-center text-h5 font-semibold') 
    
    ui.button('Example 1 iframe', on_click=lambda: ui.open(yet_another_page))
    ui.html(pag_CDP)
    
    ui.button('Example 2 new page', on_click=lambda: ui.open('sample/main-sample.html'))
    ui.html (pag_CDP_Sample)

    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        with ui.row().style('background-color: #3874c8'):
            with ui.button(on_click=lambda: menu.open()).props('icon=menu'):
                with ui.menu() as menu:
                    ui.menu_item('Inicio', lambda: ui.open(pag_main), auto_close=True)
                    ui.menu_item('Diagrama por CDP', lambda: ui.open(pag_cdp), auto_close=True)
                    ui.menu_item('Busqueda por NMAP', lambda: ui.open(pag_nmap), auto_close=True)
                    ui.menu_item('Gráfica L2 (Trace Path)',lambda: ui.open(pag_tracepath), auto_close=True)
                    ui.menu_item('Diagrama por Netbox (Not implemented)',lambda:  ui.open(pag_netbox), auto_close=True)
                    ui.menu_item('Diagrama Completo y Automatizado (Not implemented)',lambda:  ui.open(pag_fulldiagram),    auto_close=True)
                    ui.separator()
                    ui.menu_item('Nuevo diagrama', lambda: ui.open(pag_newdiagram), auto_close=True)
                    ui.separator()
                    ui.menu_item('Monitoreo (Not implemented)',lambda:  ui.open(pag_monitor), auto_close=True)
                    ui.separator()
                    ui.menu_item('Close', on_click=menu.close)
            ui.label(' . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . ').tailwind('drop-shadow', 'font-bold', 'text-blue-500')
            ui.label('  Sistema de Moniteo, Control y Recuperacion ').classes(' text-h5 font-semibold') 
            ui.label(' . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . ').tailwind('drop-shadow', 'font-bold', 'text-blue-500')
            ui.html('<img src="imgs/Escudo OEA.png" alt="JID-OEA" width="60px" />')
            ui.html('<img src="imgs/Escudo JID.png" alt="JID-OEA" width="60px" height="68"/>')
            
    with ui.left_drawer(top_corner=False, bottom_corner=False).style('background-color: #d7e3f4'):
        with ui.row().classes('w-full items-center'):    
            text_ip = ui.input(label='IP', placeholder='start typing', on_change=lambda e: result.set_text('you typed: ' + e.value), validation={'Input too long': lambda value: len(value) < 20})
            
    result = ui.label()
    print(text_ip.value )

    
######################## Pagina pag_new #########################################

@ui.page(pag_new)
async def pag_new():
    ui.label('Carga de equipos a monitorear').classes('text-h6 font-semibold') 
    ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')


    ui.label('Trace Path').classes('w-full text-center text-h5 font-semibold') 
    
    ui.button('Example 1 iframe', on_click=lambda: ui.open(pag_newdiagram))
    ui.html(pag_CDP)
    
    ui.button('Example 2 new page', on_click=lambda: ui.open('sample/main-sample.html'))
    ui.html (pag_CDP_Sample)

    [ui.label(f'Line {i}') for i in range(100)]
    
    ## Encabezado    
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        with ui.row().style('background-color: #3874c8'):
            with ui.button(on_click=lambda: menu.open()).props('icon=menu'):
                with ui.menu() as menu:
                    ui.menu_item('Inicio', lambda: ui.open(pag_main), auto_close=True)
                    ui.menu_item('Diagrama por CDP', lambda: ui.open(pag_cdp), auto_close=True)
                    ui.menu_item('Gráfica L2 (Trace Path)',lambda: ui.open(pag_tracepath), auto_close=True)
                    ui.separator()                
                    ui.menu_item('Close', on_click=menu.close)
            ui.label(' . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . ').tailwind('drop-shadow', 'font-bold', 'text-blue-500')
            ui.label('  Sistema de Moniteo, Control y Recuperacion ').classes(' text-h5 font-semibold') 
            ui.label(' . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . .  . . . . . . . . . . . . . . . ').tailwind('drop-shadow', 'font-bold', 'text-blue-500')
            ui.html('<img src="imgs/Escudo OEA.png" alt="JID-OEA" width="60px" />')
            ui.html('<img src="imgs/Escudo JID.png" alt="JID-OEA" width="60px" height="68"/>')

            
    with ui.left_drawer(top_corner=False, bottom_corner=False).style('background-color: #d7e3f4'):
        with ui.row().classes('w-full items-center'):    
            text_ip = ui.input(label='IP', placeholder='start typing', on_change=lambda e: result.set_text('you typed: ' + e.value), validation={'Input too long': lambda value: len(value) < 20})
    result = ui.label()
    print(text_ip.value )    

ui.run()



def ping_(x='127.0.0.1'):
    global rPing
    rPing = str(ping(x, verbose=False))
    return rPing
