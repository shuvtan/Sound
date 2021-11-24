import numpy as np
import matplotlib.pyplot as plt

# Функция, возвращающая скорость звука
def soundspeed(temp, h2o, co2):
	temp+=273
	
	xh2o = h2o*(1-co2)
	uh2o = 18.01*xh2o
	cph2o = 1.863*uh2o
	cvh2o = 1.403*uh2o
	
	uco2 = 44.01*co2
	cpco2 = 0.838*uco2
	cvco2 = 0.249*uco2
	
	uv = 28.97*(1-xh2o)
	cpv=1.0036*uv
	cvv=0.7166*uv
	
	y=(cpv+cph2o+cpco2)/(cvv+cvh2o+cvco2)
	
	speed=((y*8.314*temp*1000)/(uv+uh2o+uco2))**0.5
	
	return speed

# Собранные данные
temp=25.3
h2o_perc=30.7/100 # Относительная влажность
L=1.158
t1=0.00334
t2=0.00336
h2o=h2o_perc*(23/1000) # Абсолютная влажность

# Случайные погрешности
dL=0.001
dt=0.000005

try:
	# Скорости звука
	v1=L/t1
	v2=L/t2
	
	# Погрешности скоростей
	dv1=v1*((dL/L)**2+(dt/t1)**2)**0.5
	dv2=v2*((dL/L)**2+(dt/t2)**2)**0.5

	# Генерация концентраций CO2 и соответствующих им скоростей
	co2=np.linspace(0,0.05,20)
	speed=soundspeed(temp,h2o,co2)
	
	# Калибровка
	k=np.polyfit(speed,co2,1)

	# Получение значений концентраций двух случаев, пользуясь калибровочным коэффициентом
	co2_1=np.polyval(k,v1).astype(np.float32)
	co2_2=np.polyval(k,v2).astype(np.float32)
	
	# Погрешности концентраций
	dco2_1=abs(np.polyval(k,v1+dv1).astype(np.float32)-co2_1)
	dco2_2=abs(np.polyval(k,v2+dv2).astype(np.float32)-co2_2)
	
finally:

	# Сохранение обработанных данных
	info = "Коэффициент калибровки: "+str(k)+"\n\nПервый случай\nКонцентрация углекислого газа: "+str(round(co2_1*100,3))+"+-"+str(round(dco2_1*100,3))+" %\nСкорость звука: "+str(round(v1,2))+"+-"+str(round(dv1,2))+" м/с\n\nВторой случай\nКонцентрация углекислого газа: "+str(round(co2_2*100,3))+"+-"+str(round(dco2_2*100,3))+" %\nСкорость звука: "+str(round(v2,2))+"+-"+str(round(dv2,2))+" м/с"

	with open("info.txt","w") as f:
		f.write(info)
	
	# Настройка, составление и сохранение графика
	fig, ax = plt.subplots(figsize=(10,6), dpi=100)
	ax.plot(co2,speed,label="Аналитическая зависимость", linewidth=0.8)
	ax.plot(co2_1,v1,marker="*",label="Значение скорости в 1 случае: {:.2f} м/с, {:.3f} %".format(v1,co2_1),markersize=5, linewidth=0.8)
	ax.plot(co2_2,v2,marker="*",label="Значение скорости во 2 случае: {:.2f} м/с, {:.3f} %".format(v2,co2_2),markersize=5, linewidth=0.8)
	ax.set_title("Зависимость скорости звука от концентрации углекислого газа",loc="center")
	ax.set_ylabel("Скорость звука [м/с]",loc="center")
	ax.set_xlabel("Концентрация углекислого газа [%]",loc="center")
	
	fig.savefig("speed-of-sound.png")
	plt.show()