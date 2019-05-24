from django.shortcuts import render, redirect
import csv


from . import forms
from . import models
from proveedores.models import proveedor

def upload_file(request):
    if request.method == 'POST':
        form = forms.UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = models.archivo(filename = request.FILES['docfile'])
            newdoc = models.archivo(docfile = request.FILES['docfile'])
            newdoc.save(form)
            procesar_archivo(request.FILES['docfile'])
            #forms.Termine(request.POST, request.FILES)
            return render(request, 'enviarnotificacion/upload.html', {'form': form})
            #return redirect("upload")
    else:
        form = forms.UploadForm()
    #tambien se puede utilizar render_to_response
    #return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))
    return render(request, 'enviarnotificacion/upload.html', {'form': form})

def procesar_archivo(nombre):
    listaControl = []
    listaEnvio = []
    listaOperacion = []
    textoEnvioControl = "<h3>Se envio notificacion de pagos por correo electronico a los siguientes proveedores</h3>"
    textoEnvioControl += '<br></br><table BORDER bordercolor="black" CELLPADDING=10 CELLSPACING=0><tr><th>No</th><th>RAZON SOCIAL PROVEEDOR</th><th>CORREO ENVIO NOTIFICACION</th></tr>'
    noEnviado=""
    y=0
    #ruta='upload\'+models.archivo.filename()

    with open('upload\%s' % nombre) as csvarchivo:
    #with open('upload\docOrigen-.csv') as csvarchivo:
        entrada = csv.reader(csvarchivo)
        #print("------> %s " % csv.reader(csvarchivo))
        textoEnvio = ""

        for reg in entrada:
            if reg[0] in listaControl:
                textoEnvio += "<tr><td ALIGN=right>" + reg[3] + "</td><td ALIGN=right>" + reg[8] + "</td><td ALIGN=right>" + reg[4] + "</td><td ALIGN=right>" + reg[5] + "</td><td ALIGN=right>" + reg[6] + "</td><td ALIGN=right>" + reg[7] + "</td></tr>"
            else:
                if textoEnvio:
                    textoEnvio += "</table><br></br><br></br><p>Agradecemos distribuir esta informacion al personal de su empresa que le puedan ser util estos datos.</p>"
                    textoEnvio += "<br></br><br></br><footer><strong>POR FAVOR NO RESPONDER A ESTA CUENTA DE CORREO, NADIE MONITOREA ESTOS MENSAJES Y SE ELIMINAN AUTOMATICAMENTE.</strong></footer>"
                    listaEnvio.append(textoEnvio)
                    textoEnvio = ""

                listaControl.append(reg[0])
                textoEnvio += "<h3>Cordial Saludo.</h3>"
                textoEnvio += "<br></br><h3>Industrias Astivik le informa, que se realizo una transferencia el dia " + reg[2] + " a su cuenta bancaria No " + reg[1] + "</h3>"
                textoEnvio += "<br></br><p>Las facturas pagadas fueron las siguientes:</p>"
                textoEnvio += '<br></br><table BORDER bordercolor="black" CELLPADDING=10 CELLSPACING=0><tr><th>No FACTURA</th><th>VALOR NETO FACTURA</th><th>VALOR RET ICA</th><th>VALOR RET IVA</th><th>VALOR RET RENTA</th><th>VALOR PAGADO</th></tr>'
                textoEnvio += "<tr><td>" + reg[3] + "</td><td ALIGN=right>" + reg[8] + "</td><td ALIGN=right>" + reg[4] + "</td><td ALIGN=right>" + reg[5] + "</td><td ALIGN=right>" + reg[6] + "</td><td ALIGN=right>" + reg[7] + "</td></tr>"

        textoEnvio += "</table><br></br><br></br></p>Agradecemos distribuir esta informacion al personal de su empresa que le puedan ser util estos datos.</p>"
        textoEnvio += "<br></br><br></br><footer><strong>POR FAVOR NO RESPONDER A ESTA CUENTA DE CORREO, NADIE MONITOREA ESTOS MENSAJES Y SE ELIMINAN AUTOMATICAMENTE.</strong></footer>"
        listaEnvio.append(textoEnvio)

    #print ("TOTAL REGISTROS A PROCESAR %d " % (len(listaControl)))

    try:
        for i in range(len(listaControl)):
            listaOperacion = proveedor.objects.filter(nit="%s" % listaControl[i])
            #proveedores = proveedor.objects.filter(nit="%s" % listaControl[i])
            #Bd2.main(listaControl[i])
            #print ("LISTA OPERACION %d " % (len(listaOperacion)))
            #print ("LISTA CONTROL I %d " % (len(listaControl[i])))
            x=0
            
            for filas in listaOperacion:
                if not filas:
                    noEnviado+= "<br></br>"+((listaControl[i]))
                    #print ("NO SE PUDO ENVIAR CORREO A %s " % ((listaControl[i])))
                else:
                    if filas[2]:
                        y+=1
                        try:
                            models.envioCorreo("info@astivik.com.co", (filas[x+2]), listaEnvio[i])
                            textoEnvioControl += "<tr><td ALIGN=center>" + str(y) + "</td><td ALIGN=left>" + (filas[x+1]) + "</td><td ALIGN=left>" + (filas[x+2]) + "</td></tr>"
                            #print ("SE ENVIO CORREO A %s -- %s al correo %s " % ((filas[x]), (filas[x+1]), (filas[x+2])))
                        except Exception as ex:
                            print ("NO ----------- %s " % ((listaControl[i])))
                    else:
                        noEnviado+= "<br></br>"+(filas[x])+" -- "+(filas[x+1])
                        #print ("PROVEEDOR NO TIENE GUARDADO NINGUN CORREO ELECTRONICO %s -- %s " % ((filas[x]), (filas[x+1])))
                x+=3
    except Exception as ex:
        print ("MainException ----------- %s " % (ex))

    textoEnvioControl += "</table><br></br><br></br><p>A algunos proveedores no se les pudo enviar notificacion por que no tienen asignado actualmente una direccion de correo electronico en la base de datos de notificaciones.</p>"+noEnviado
    models.envioCorreo("sistemas@astivik.com.co", "auxcontable@astivik.com.co", textoEnvioControl)
    models.envioCorreo("sistemas@astivik.com.co", "contabilidad@astivik.com.co", textoEnvioControl)
    models.envioCorreo("sistemas@astivik.com.co", "sistemas@astivik.com.co", textoEnvioControl)