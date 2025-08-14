% 12 09 19
% 
%
clear

raizDos=sqrt(2);
format bank


nombre= input('indica el nombre entre comillas y con su extension   ')
%indiceNombre=input('indica el indice del nombre de acuerdo al orden de voluntarios ')
%indiceCarga=input('indica el valor de la carga ')



AA=load(nombre,'-ascii');
RR=AA(:,2);

%los siguientes parametros permitiran recorrer todo el arreglo RR 
tama=size(RR);
tamRR=tama(1);

% las siguientes variables son de control para encontrar las porciones 
% del arreglo que llegan hasta algun valor del tiempo en minutos
contador1=0; contador5=0; contador6=0;
contador7=0; contador9=0; contador14=0;
contador18=0; contador20=0; contador30=0;
contador19=0; contador31=0; contador25=0;


% las siguientes instrucciones eliminan del arreglo los valores que valen
%  cero, y encuentran en que lugares del arreglo se cumple un
% cierto intervalo de tiempo. Ademas se introduce un arreglo de tiempo para
% el eje temporal de las figuras.

ijk=0;
for ii=1:tamRR
    if (RR(ii)>0)
    
    ijk=ijk+1;
    nRR(ijk)=RR(ii);
    
    ejeTiempoMinutos(ijk)=AA(ii,1);
    
     if ((contador1==0)&&(ejeTiempoMinutos(ijk)>1))
        ijk1=ijk;
        contador1=1;
     end
     if ((contador5==0)&&(ejeTiempoMinutos(ijk)>5))
        ijk5=ijk;
        contador5=1;
    end
     if ((contador6==0)&&(ejeTiempoMinutos(ijk)>6))
        ijk6=ijk;
        contador6=1;
     end
    
    if ((contador7==0)&&(ejeTiempoMinutos(ijk)>7))
        ijk7=ijk;
        contador7=1;
    end
    if ((contador9==0)&&(ejeTiempoMinutos(ijk)>9))
        ijk9=ijk;
        contador9=1;
    end
     if ((contador18==0)&&(ejeTiempoMinutos(ijk)>18))
        ijk18=ijk;
        contador18=1;
     end
    if ((contador19==0)&&(ejeTiempoMinutos(ijk)>19))
        ijk19=ijk;
        contador19=1;
    end
     if ((contador20==0)&&(ejeTiempoMinutos(ijk)>20))
        ijk20=ijk;
        contador20=1;
    end
    if ((contador14==0)&&(ejeTiempoMinutos(ijk)>14))
        ijk14=ijk;
        contador14=1;
    end    
    if ((contador25==0)&&(ejeTiempoMinutos(ijk)>25))
        ijk25=ijk;
        contador25=1;
    end  
    if ((contador30==0)&&(ejeTiempoMinutos(ijk)>30))
        ijk30=ijk;
        contador30=1;
    end
    if ((contador31==0)&&(ejeTiempoMinutos(ijk)>31))
        ijk31=ijk;
        contador31=1;
    end   
    end
end



tama_nRR=size(nRR);
tam_nRR=tama_nRR(2);

% se renombra el arreglo, solo por usar un codigo anteriormente escrito
RR=nRR;
   




% las siguientes instrucciones encuentran promedios y desviaciones estandar
% de los intervalos entre latidos para algunos segmentos temporales. p para
% promedio y v para desviación estandar
pRepMin1a6=mean(RR(ijk1:ijk6));
vRepMin1a6=std(RR(ijk1:ijk6));
%pRepMin5a6=mean(RR(ijk5:ijk6));
%vRepMin5a6=std(RR(ijk5:ijk6));
pEjerMin14a19=mean(RR(ijk14:ijk19));
vEjerMin14a19=std(RR(ijk14:ijk19));
%pEjerMin18a19=mean(RR(ijk18:ijk19));
%vEjerMin18a19=std(RR(ijk18:ijk19));
pRecMin25a30=mean(RR(ijk25:ijk30));
vRecMin25a30=std(RR(ijk25:ijk30));
%pRecMin30a31=mean(RR(ijk30:ijk31));
%vRecMin30a31=std(RR(ijk30:ijk31));

% la instrucción line pinta lineas para dividir temporalmente la grafica.
figure
plot(ejeTiempoMinutos,nRR,'.')
hold on
line([7 7],[200 1200],'Color','k')
line([9 9],[200 1200],'Color','k')
line([20 20],[200 1200],'Color','k')
line([0 35],[400 400],'Color','r')
line([0 35],[600 600],'Color','k')
line([0 35],[800 800],'Color','k')
line([0 35],[1000 1000],'Color','k')
line([1 1],[200 1200],'Color','g')
line([6 6],[200 1200],'Color','g')
line([14 14],[200 1200],'Color','g')
line([19 19],[200 1200],'Color','g')
line([25 25],[200 1200],'Color','g')
line([30 30],[200 1200],'Color','g')
%axis([0 35 200 1300])
buss2=num2str(vRepMin1a6);
text(2,1200,buss2)
buss1=num2str(pRepMin1a6);
text(2,300,buss1)
%buss=num2str(vRepMin5a6);
%text(2,1150,buss)
%buss=num2str(pRepMin5a6);
%text(2,250,buss)
buss4=num2str(vEjerMin14a19);
text(10,1200,buss4)
buss3=num2str(pEjerMin14a19);
text(10,300,buss3)
% buss=num2str(vEjerMin18a19);
% text(10,1150,buss)
% buss=num2str(pEjerMin18a19);
% text(10,250,buss)
buss6=num2str(vRecMin25a30);
text(22,1200,buss6)
buss5=num2str(pRecMin25a30);
text(22,300,buss5)
% buss=num2str(vRecMin30a31);
% text(22,1150,buss)
% buss=num2str(pRecMin30a31);
% text(22,250,buss)
text(30,1250,'VFC')
text(30,1200,'5 min')
%text(30,1150,'1 min')
text(30,350,'pro RR')
text(30,300,'5 min')
%text(30,250,'1 min')
title(nombre)
xlabel('tiempo (minutos)')
ylabel('RR (ms)')

% 
 
%'para continuar dar ENTER de otra manera control c  '
%pause

% figure
 
 
 % a continuacion hay cuatro bloques para calcular los parametros SD1 y SD2
 % (que son el ancho y el largo de la elipse de puntos) para cada parte del
 % protocolo: reposo, calentamiento, ejercicio y recuperación
 

 
 % comienza sección de reposo (7 minutos)
 serieREP=RR(ijk1:ijk7);


clear tami taman zzz Mzzz caso otraM persistenciaMayor
tami=size(serieREP);
taman=tami(2);
tamanoREP=taman;
%zzz=serieREP;

%%%%%%%%%%% calculo de SD1 y SD2
clear sumaTemp bas0 bas1
serieREPpro=mean(serieREP);

sumaTemp=0;
for izk=1:taman-1
    bas0=(serieREP(izk)-serieREP(izk+1))/raizDos;
    bas1=bas0*bas0;
    sumaTemp=sumaTemp+bas1;
end
SD1rep = sqrt ( (1/(taman-1)) * sumaTemp );

clear sumaTemp bas0 bas1
sumaTemp=0;
for izk=1:taman-1
    bas0=(serieREP(izk)+serieREP(izk+1)-2*serieREPpro)/raizDos;
    bas1=bas0*bas0;
    sumaTemp=sumaTemp+bas1;
end
SD2rep = sqrt ( (1/(taman-1)) * sumaTemp );

% termina sección de reposo

%comienza sección de calentamiento

%pause
serieCalen=RR(ijk7:ijk9);


clear tami taman zzz Mzzz caso otraM persistenciaMayor
tami=size(serieCalen);
taman=tami(2);
tamanoCalen=taman;


%%%%%%%%%%% calculo de SD1 y SD2
clear sumaTemp bas0 bas1
serieCalenpro=mean(serieCalen);

sumaTemp=0;
for izk=1:taman-1
    bas0=(serieCalen(izk)-serieCalen(izk+1))/raizDos;
    bas1=bas0*bas0;
    sumaTemp=sumaTemp+bas1;
end
SD1calen = sqrt ( (1/(taman-1)) * sumaTemp );

clear sumaTemp bas0 bas1
sumaTemp=0;
for izk=1:taman-1
    bas0=(serieCalen(izk)+serieCalen(izk+1)-2*serieCalenpro)/raizDos;
    bas1=bas0*bas0;
    sumaTemp=sumaTemp+bas1;
end
SD2Calen = sqrt ( (1/(taman-1)) * sumaTemp );

%termina sección de calentamiento (2 minutos)

% comienza sección de ejercicio ( 11 minutos)

%pause
serieEJER=RR(ijk9:ijk20);


clear tami taman zzz Mzzz caso otraM persistenciaMayor
tami=size(serieEJER);
taman=tami(2);
tamanoEJER=taman;
%%%%%%%%%%% calculo de SD1 y SD2
clear sumaTemp bas0 bas1
serieEJERpro=mean(serieEJER);

sumaTemp=0;
for izk=1:taman-1
    bas0=(serieEJER(izk)-serieEJER(izk+1))/raizDos;
    bas1=bas0*bas0;
    sumaTemp=sumaTemp+bas1;
end
SD1ejer = sqrt ( (1/(taman-1)) * sumaTemp );

clear sumaTemp bas0 bas1
sumaTemp=0;
for izk=1:taman-1
    bas0=(serieEJER(izk)+serieEJER(izk+1)-2*serieEJERpro)/raizDos;
    bas1=bas0*bas0;
    sumaTemp=sumaTemp+bas1;
end
SD2ejer = sqrt ( (1/(taman-1)) * sumaTemp );

%termina sección de ejercicio


% comienza sección de recuperación (10 minutos)

serieREC=RR(ijk20:ijk30);

% 
clear tami taman zzz Mzzz caso otraM persistenciaMayor
tami=size(serieREC);
taman=tami(2);
tamanoREC=taman;
% %%%%%%%%%%% calculo de SD1 y SD2
 clear sumaTemp bas0 bas1
 serieRECpro=mean(serieREC);
% 
 sumaTemp=0;
 for izk=1:taman-1
     bas0=(serieREC(izk)-serieREC(izk+1))/raizDos;
     bas1=bas0*bas0;
     sumaTemp=sumaTemp+bas1;
 end
 SD1rec = sqrt ( (1/(taman-1)) * sumaTemp );
% 
 clear sumaTemp bas0 bas1
 sumaTemp=0;
 for izk=1:taman-1
     bas0=(serieREC(izk)+serieREC(izk+1)-2*serieRECpro)/raizDos;
     bas1=bas0*bas0;
     sumaTemp=sumaTemp+bas1;
 end
 SD2rec = sqrt ( (1/(taman-1)) * sumaTemp );
% 
% termina sección de recuperación


% se hace una figura para cada parte del proceso y una para todos juntos.
% Cada RR es primero coordenada x, luego coordenada y.

figure
axis([300 1200 300 1200])
hold on
for cvc=1:tamanoREP-1
    plot(serieREP(cvc),serieREP(cvc+1),'b.')
%    pause(0.2)
   % plot(serieREP(cvc),serieREP(cvc+1),'b.')
end
pause
for cvc=1:tamanoCalen-1
    plot(serieCalen(cvc),serieCalen(cvc+1),'g.')
 %   pause(0.2)
end
pause
for cvc=1:tamanoEJER-1
    plot(serieEJER(cvc),serieEJER(cvc+1),'r.')
  %  pause(0.2)
end
pause
for cvc=1:tamanoREC-1
    plot(serieREC(cvc),serieREC(cvc+1),'y.')
  %  pause(0.2)
end
pause

%pause

figure
hold on
for cvc=1:tamanoREP-1
    plot(serieREP(cvc),serieREP(cvc+1),'b.')
%    pause(0.2)axis([300 1200 300 1200])
   % plot(serieREP(cvc),serieREP(cvc+1),'b.')
end
axis([300 1200 300 1200])
figure
hold on
for cvc=1:tamanoCalen-1
    plot(serieCalen(cvc),serieCalen(cvc+1),'g.')
 %   pause(0.2)
end
axis([300 1200 300 1200])
figure
hold on
for cvc=1:tamanoEJER-1
    plot(serieEJER(cvc),serieEJER(cvc+1),'r.')
  %  pause(0.2)
end
axis([300 1200 300 1200])
figure
hold on
for cvc=1:tamanoREC-1
    plot(serieREC(cvc),serieREC(cvc+1),'y.')
  %  pause(0.2)
end
axis([300 1200 300 1200])




[ SD1rep SD2rep SD1ejer SD2ejer SD1rec SD2rec]