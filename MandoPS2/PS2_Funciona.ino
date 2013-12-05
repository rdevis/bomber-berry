#include <PS2X_lib.h>

PS2X ps1x, ps2x;

unsigned char ps1Analog[4]={0};
unsigned char ps2Analog[4]={0};
int error = 0, indice = 0, i=0;
byte vibrate = 0;
boolean enviadoPS1[24]={false}, enviadoPS2[24]={false};
char entrada = 0;

void setup()
{
  Serial.begin(57600); //Inicia la comunicación serie a 57600 baudios
  error = ps1x.config_gamepad(13,11,10,12, false, false); //Configura el mando (13 --> CLK // 12 --> DATA // 11 --> CMD // 10 --> ATT) Sin modo analógico // Sin vibración
 
  if(error == 0)
    Serial.println("Mando 1: Encontrado y conectado correctamente");   

  else if(error == 1)
    Serial.println("Mando 1: No se ha encontrado ningun controlador, revisa que no la hayas liado parda con los cables");
   
  else if(error == 2)
    Serial.println("Mando 1: Controlador encontrado pero rechaza los comandos");
   
  else if(error == 3)
    Serial.println("Mando 1: Imposible entrar al modo presion del mando");
    
  error = ps2x.config_gamepad(9,7,6,8, false, false); //Configura el mando (9 --> CLK // 8 --> DATA // 7 --> CMD // 6 --> ATT) Sin modo analógico // Sin vibración

  if(error == 0)
    Serial.println("Mando 2: Encontrado y conectado correctamente");   

  else if(error == 1)
    Serial.println("Mando 2: No se ha encontrado ningun controlador, revisa que no la hayas liado parda con los cables");
   
  else if(error == 2)
    Serial.println("Mando 2: Controlador encontrado pero rechaza los comandos");
   
  else if(error == 3)
    Serial.println("Mando 2: Imposible entrar al modo presion del mando");
  
}

void loop()
{ 
  if(error == 1) //Si no ha conectado con el mando ahorrate el loop
  return; 
  
  while(Serial.available() > 0)
  {
    switch (indice)
    {
      case 0:
        entrada = Serial.read();
        if (entrada == ';')
           indice = 1;
        break;
     
      case 1:
        entrada = Serial.read();
        if (entrada == '1')
          indice = 2;
        else if (entrada == '2')
          indice = 3;
        else if (entrada == ';')
          indice = 1;
        else
          indice = 0;
        break;
        
      case 2:
        entrada = Serial.read();
        if (entrada == 'R')
          indice = 4;
        else if (entrada == 'V')
          indice = 5;
        else if (entrada == ';')
          indice = 1;
        else
          indice = 0;
        break;
          
      case 3:
        entrada = Serial.read();
        if (entrada == 'R')
          indice = 6;
        else if (entrada == 'V')
          indice = 7;
        else if (entrada == ';')
          indice = 1;
        else
          indice = 0;
        break;
       
       case 4:
         entrada = Serial.read();
         if (entrada == 'E')
           indice = 8;
         else if (entrada == ';')
           indice = 1;
         else
           indice = 0;
         break;
         
       case 5:
         entrada = Serial.read();
         if (entrada == '1')
           indice = 9;
         else if (entrada == '0')
           indice = 10;
         else if (entrada == ';')
           indice = 1;
         else
           indice = 0;
         break;
         
       case 6:
         entrada = Serial.read();
         if (entrada == 'E')
           indice = 11;
         else if (entrada == ';')
           indice = 1;
         else
           indice = 0;
         break;
         
       case 7:
         entrada = Serial.read();
         if (entrada == '1')
           indice = 12;
         else if (entrada == '0')
           indice = 13;
         else if (entrada == ';')
           indice = 1;
         else
           indice = 0;
         break;
       
       case 8:
         entrada = Serial.read();
         if (entrada == ':')
         {
            //PONER AQUI EL CODIGO PARA RESETEAR MEMORIA MANDO 1  
            for(i=0; i<24; i++)
              enviadoPS1[i]=false;
            indice = 0;
         }
         else if (entrada == ';')
           indice = 1;
         else
           indice = 0;
         break;
         
       case 9:
         entrada = Serial.read();
         if (entrada == ':')
         {
            //PONER AQUI EL CODIGO PARA ENCENDER LA VIBRACION DEL MANDO 1
            indice = 0;
         }
         else if (entrada == ';')
           indice = 1;
         else
           indice = 0;
         break; 
 
       case 10:
         entrada = Serial.read();
         if (entrada == ':')
         {
            //PONER AQUI EL CODIGO PARA APAGAR LA VIBRACION DEL MANDO 1
            indice = 0;
         }
         else if (entrada == ';')
           indice = 1;
         else
           indice = 0;
         break;   
   
       case 11:
         entrada = Serial.read();
         if (entrada == ':')
         {
            //PONER AQUI EL CODIGO PARA RESETEAR MEMORIA MANDO 2  
            for(i=0; i<24; i++)
              enviadoPS2[i]=false;
            indice = 0;
         }
         else if (entrada == ';')
           indice = 1;
         else
           indice = 0;
         break;  
     
       case 12:
         entrada = Serial.read();
         if (entrada == ':')
         {
            //PONER AQUI EL CODIGO PARA ENCENDER LA VIBRACION DEL MANDO 2
            indice = 0;
         }
         else if (entrada == ';')
           indice = 1;
         else
           indice = 0;
         break;   
      
       case 13:
         entrada = Serial.read();
         if (entrada == ':')
         {
            //PONER AQUI EL CODIGO PARA APAGAR LA VIBRACION DEL MANDO 1
            indice = 0;
         }
         else if (entrada == ';')
           indice = 1;
         else
           indice = 0;
         break; 
       
       default:
         indice = 0;
         break;
    }
  }  
  
  ps1x.read_gamepad(false, vibrate);          //Lee el mando y le manda la velocidad de vibracion
  
  ps1Analog[0]=ps1x.Analog(PSS_LY);
  if(ps1Analog[0]>200 && enviadoPS1[16]==false)
  {
    Serial.print(";1LD:\r");
    enviadoPS1[16]=true;      
  }
  else if(ps1Analog[0]<55 && enviadoPS1[17]==false)
  {
    Serial.print(";1LU:\r");
    enviadoPS1[17]=true;      
  }
  ps1Analog[1]=ps1x.Analog(PSS_LX);
  if(ps1Analog[1]>200 && enviadoPS1[18]==false)
  {
    Serial.print(";1LR:\r");
    enviadoPS1[18]=true;      
  }
  else if(ps1Analog[1]<55 && enviadoPS1[19]==false)
  {
    Serial.print(";1LL:\r");
    enviadoPS1[19]=true;
  }
    
  ps1Analog[2]=ps1x.Analog(PSS_RY);
  if(ps1Analog[2]>200 && enviadoPS1[20]==false)
  {
    Serial.print(";1RD:\r");
    enviadoPS1[20]=true;
  }
  else if(ps1Analog[2]<55 && enviadoPS1[21]==false)
  {
    Serial.print(";1RU:\r");
    enviadoPS1[21]=true;
  }
  ps1Analog[3]=ps1x.Analog(PSS_RX);
  if(ps1Analog[3]>200 && enviadoPS1[22]==false)
  {
    Serial.print(";1RR:\r");
    enviadoPS1[22]=true;
  }
  else if(ps1Analog[3]<55 && enviadoPS1[23]==false)
  {
    Serial.print(";1RL:\r");
    enviadoPS1[23]=true;
  }
  
  if(ps1x.Button(PSB_START) && enviadoPS1[0]==false)
  {  
    Serial.print(";1ST:\r");
    enviadoPS1[0]=true;
  }
       
  if(ps1x.Button(PSB_SELECT) && enviadoPS1[1]==false)
  {
    Serial.print(";1SE:\r");
    enviadoPS1[1]=true;
  }
       
  if(ps1x.Button(PSB_GREEN) && enviadoPS1[2]==false)
  {
    Serial.print(";1TR:\r");
    enviadoPS1[2]=true;
  }
  
  if(ps1x.Button(PSB_RED) && enviadoPS1[3]==false)
  {
    Serial.print(";1CI:\r");
    enviadoPS1[3]=true;
  }
       
  if(ps1x.Button(PSB_PINK) && enviadoPS1[4]==false)     
  {  
    Serial.print(";1CU:\r");     
    enviadoPS1[4]=true;
  }
  
  if(ps1x.Button(PSB_BLUE) && enviadoPS1[5]==false)
  {  
    Serial.print(";1EQ:\r");    
    enviadoPS1[5]=true;
  }
       
  if(ps1x.Button(PSB_L1) && enviadoPS1[6]==false)
  {
    Serial.print(";1L1:\r");
    enviadoPS1[6]=true;
  }
  
  if(ps1x.Button(PSB_R1) && enviadoPS1[7]==false)
  {
    Serial.print(";1R1:\r");
    enviadoPS1[7]=true;
  }

  if(ps1x.Button(PSB_L2) && enviadoPS1[8]==false)
  {
    Serial.print(";1L2:\r");
    enviadoPS1[8]=true;
  }
  
  if(ps1x.Button(PSB_R2) && enviadoPS1[9]==false)
  {
    Serial.print(";1R2:\r");
    enviadoPS1[9]=true;
  }
    
  if(ps1x.Button(PSB_L3) && enviadoPS1[10]==false)
  {
    Serial.print(";1L3:\r");
    enviadoPS1[10]=true;
  }
    
  if(ps1x.Button(PSB_R3) && enviadoPS1[11]==false)
  {
    Serial.print(";1R3:\r");
    enviadoPS1[11]=true;
  }

  if(ps1x.Button(PSB_PAD_UP) && enviadoPS1[12]==false)
  {
    Serial.print(";1AR:\r");
    enviadoPS1[12]=true;
  }
  
  if(ps1x.Button(PSB_PAD_DOWN) && enviadoPS1[13]==false)
  {
    Serial.print(";1AB:\r");
    enviadoPS1[13]=true;
  }
    
  if(ps1x.Button(PSB_PAD_LEFT) && enviadoPS1[14]==false)
  {
    Serial.print(";1IZ:\r");
    enviadoPS1[14]=true;
  }
    
  if(ps1x.Button(PSB_PAD_RIGHT) && enviadoPS1[15]==false)
  {
    Serial.print(";1DE:\r");    
    enviadoPS1[15]=true;
  }
  
//--------------------------------------------------------------------------------

  ps2x.read_gamepad(false, vibrate);          //Lee el mando y le manda la velocidad de vibracion
  
  ps2Analog[0]=ps2x.Analog(PSS_LY);
  if(ps2Analog[0]>200 && enviadoPS2[16]==false)
  {
    Serial.print(";2LD:\r");
    enviadoPS2[16]=true;      
  }
  else if(ps2Analog[0]<55 && enviadoPS2[17]==false)
  {
    Serial.print(";2LU:\r");
    enviadoPS2[17]=true;      
  }
  ps2Analog[1]=ps2x.Analog(PSS_LX);
  if(ps2Analog[1]>200 && enviadoPS2[18]==false)
  {
    Serial.print(";2LR:\r");
    enviadoPS2[18]=true;      
  }
  else if(ps2Analog[1]<55 && enviadoPS2[19]==false)
  {
    Serial.print(";2LL:\r");
    enviadoPS2[19]=true;
  }
    
  ps2Analog[2]=ps2x.Analog(PSS_RY);
  if(ps2Analog[2]>200 && enviadoPS2[20]==false)
  {
    Serial.print(";2RD:\r");
    enviadoPS2[20]=true;
  }
  else if(ps2Analog[2]<55 && enviadoPS2[21]==false)
  {
    Serial.print(";2RU:\r");
    enviadoPS2[21]=true;
  }
  ps2Analog[3]=ps2x.Analog(PSS_RX);
  if(ps2Analog[3]>200 && enviadoPS2[22]==false)
  {
    Serial.print(";2RR:\r");
    enviadoPS2[22]=true;
  }
  else if(ps2Analog[3]<55 && enviadoPS2[23]==false)
  {
    Serial.print(";2RL:\r");
    enviadoPS2[23]=true;
  }
  
  if(ps2x.Button(PSB_START) && enviadoPS2[0]==false)
  {  
    Serial.print(";2ST:\r");
    enviadoPS2[0]=true;
  }
       
  if(ps2x.Button(PSB_SELECT) && enviadoPS2[1]==false)
  {
    Serial.print(";2SE:\r");
    enviadoPS2[1]=true;
  }
       
  if(ps2x.Button(PSB_GREEN) && enviadoPS2[2]==false)
  {
    Serial.print(";2TR:\r");
    enviadoPS2[2]=true;
  }
  
  if(ps2x.Button(PSB_RED) && enviadoPS2[3]==false)
  {
    Serial.print(";2CI:\r");
    enviadoPS2[3]=true;
  }
       
  if(ps2x.Button(PSB_PINK) && enviadoPS2[4]==false)     
  {  
    Serial.print(";2CU:\r");     
    enviadoPS2[4]=true;
  }
  
  if(ps2x.Button(PSB_BLUE) && enviadoPS2[5]==false)
  {  
    Serial.print(";2EQ:\r");    
    enviadoPS2[5]=true;
  }
       
  if(ps2x.Button(PSB_L1) && enviadoPS2[6]==false)
  {
    Serial.print(";2L1:\r");
    enviadoPS2[6]=true;
  }
  
  if(ps2x.Button(PSB_R1) && enviadoPS2[7]==false)
  {
    Serial.print(";2R1:\r");
    enviadoPS2[7]=true;
  }

  if(ps2x.Button(PSB_L2) && enviadoPS2[8]==false)
  {
    Serial.print(";2L2:\r");
    enviadoPS2[8]=true;
  }
  
  if(ps2x.Button(PSB_R2) && enviadoPS2[9]==false)
  {
    Serial.print(";2R2:\r");
    enviadoPS2[9]=true;
  }
    
  if(ps2x.Button(PSB_L3) && enviadoPS2[10]==false)
  {
    Serial.print(";2L3:\r");
    enviadoPS2[10]=true;
  }
    
  if(ps2x.Button(PSB_R3) && enviadoPS2[11]==false)
  {
    Serial.print(";2R3:\r");
    enviadoPS2[11]=true;
  }

  if(ps2x.Button(PSB_PAD_UP) && enviadoPS2[12]==false)
  {
    Serial.print(";2AR:\r");
    enviadoPS2[12]=true;
  }
  
  if(ps2x.Button(PSB_PAD_DOWN) && enviadoPS2[13]==false)
  {
    Serial.print(";2AB:\r");
    enviadoPS2[13]=true;
  }
    
  if(ps2x.Button(PSB_PAD_LEFT) && enviadoPS2[14]==false)
  {
    Serial.print(";2IZ:\r");
    enviadoPS2[14]=true;
  }
    
  if(ps2x.Button(PSB_PAD_RIGHT) && enviadoPS2[15]==false)
  {
    Serial.print(";2DE:\r");    
    enviadoPS2[15]=true;
  }
  
  delay(10);
     
}
