
var myModal = new bootstrap.Modal(document.getElementById('exampleModal'),{backdrop:false})
var elem2 = document.querySelector('#eden1');
var rangeValue2 = function(){
var newValue2 = elem2.value;
var target2 = document.querySelector('#eden');
target2.innerHTML = newValue2;
}
elem2.addEventListener("input", rangeValue2);
var elem = document.querySelector('#salproi');
var rangeValue = function(){
// console.log(elem.value);
// if((elem.value * 1) >= 2150){
// elem.setAttribute("step", "10");
// } else {
// elem.setAttribute("step", "100");
// }
var newValue = "$"+elem.value;
var target = document.querySelector('#salpro');
target.innerHTML = newValue;
}
elem.addEventListener("input", rangeValue);
var elem3 = document.querySelector('#semco1');
var rangeValue3 = function(){
var rangeValue3 = elem3.value;
var target3 = document.querySelector('#semco');
target3.innerHTML = rangeValue3;
}
elem3.addEventListener("input", rangeValue3);
var correoSi = document.querySelector('#input1');
var nombreSi = document.querySelector('#input2');
var correoSi = document.querySelector('#input1');
var nombreSi = document.querySelector('#input2');
function submiteando(){
var OnSalProm =elem.value;
var OnEdad = elem2.value;
var OnSemCot = elem3.value;
var Calculo = CalcPen(OnSalProm, OnEdad, OnSemCot);
var modalLoading = document.getElementById("loadingModal");
modalLoading.setAttribute("style", "display: block;");
document.getElementsByTagName("body")[0].classList.add("modal-open");
// myModal.toggle() pEnviado modal-open loadingModal
//alert("Tus HOLA ---> Correo: "+correoSi.value+" | " + "Nombre: "+ nombreSi.value +" | Edad: "+ elem2.value + " | Salario: "+ elem.value +" | Semanas: " +elem3.value + "| Calculo APROX:" +Calculo)
fetch(`https://humana.mx/api-v1/?Nombre=${nombreSi.value}&Correo=${correoSi.value}&Edad=${elem2.value}&Salario=${elem.value}&Semanas=${elem3.value}&Calculo=${Calculo}`)
.then(response => {
modalLoading.setAttribute("style", "display: none;");
// console.log(response)
if (response.status === 200) {
var soyPP = document.getElementById("pEnviado");
soyPP.innerHTML = 'Edad <strong>'+elem2.value+'</strong>; Salario Promedio <strong>'+elem.value+'</strong>; Semanas Cotizadas <strong>'+elem3.value+'</strong>.';
myModal.toggle()
}
})
}
function CalcPen(input1, input2, input3){
//alert("Tus HOLA ---> Correo: "+correoSi.value+" | " + "Nombre: "+ nombreSi.value +" | Edad: "+ elem2.value + " | Salario: "+ elem.value +" | Semanas: " +elem3.value)
var SalProm = parseInt(input1);
var Edad =  parseInt(input2);
var SemCot =  parseInt(input3);
// console.log("estos son lso datos a calcular", SalProm, Edad, SemCot );


//Pestaña tablas
var tablaVSMi = [0, 1.01, 1.26, 1.51, 1.76, 2.01, 2.26, 2.51, 2.76, 3.01, 3.26, 3.51, 3.76, 4.01, 4.26, 4.51, 4.76, 5.01, 5.26, 5.51, 5.76, 6.01]
var tablaVSMx = [1, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00, 4.25, 4.50, 4.75, 5.00, 5.25, 5.50, 5.75, 6.00, 25.00]
var tablaCB  = [.8000, .7711, .5818, .4923, .4267, .3765, .3368, .3048, .2783, .2560, .2370, .2207, .2065, .1939, .1829, .1730, .1641, .1561, .1488, .1422, .1362, .1300]
var tablaIncr = [.005630, .008140, .01178, .01430, .01615, .01756, .01868, .01958, .02033, .02096, .02149, .02195, .02235, .02271, .02302, .02330, .02355, .02377, .02398, .02416, .02433, .02450]

//Pestaña cálculo
var tablaEdades = [55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]
var tablaPorc = [.75, .75, .75, .75, .75, .75, .80, .85, .90, .95, 1]


var SalVSM = SalProm / 89.62 ;
for (var i = 0; i < tablaVSMi.length; i++) {
if (tablaVSMi[i] <= SalVSM && tablaVSMx [i] >= SalVSM ) {
var CB = tablaCB[i];
var Incr = tablaIncr[i];
}
}
var OpSem = (SemCot-500)/52
var OpSemInt = parseInt(OpSem);
var OpSemDec = OpSem - OpSemInt;
for (var i = 0; i<4; i++){
if (OpSemDec ==0 || OpSemDec < .2307692399){
var OpSemRed = 0;
} else if (OpSemDec > .2307692400 && OpSemDec < .4807692400){
var OpSemRed = .5;
} else {
var OpSemRed = 1;
}
}
var Incrmnto = OpSemInt + OpSemRed;
var AnualIncr = ((SalProm*365)*Incr)*Incrmnto;
var AnualCoti = (SalProm*365)*CB;
var AnualPension = (AnualIncr + AnualCoti)*1.15;
var AnualPensionFox = AnualPension*1.11;
var MensualPension =AnualPensionFox/12;
var Oporc;
for ( var i=0; i < tablaEdades.length; i++){
if (tablaEdades[i] == Edad){
var Oporc = tablaPorc[i]; }
}
var CalcPension = MensualPension*Oporc;
var CalcPensionR = CalcPension + .01;
var PaseCalcPension = Math.round(CalcPensionR);
var dig1=PaseCalcPension%10;
var realres=PaseCalcPension - dig1;
var Op1=realres/10;
var dig2=Op1%10;
var realres2=Op1-dig2;
var Op2=realres2/10;
var dig3=Op2%10;
var digito1=dig1;
var digito2=dig2*10;
var digito3=dig3*100;
var SumaDig=digito1+digito2+digito3;
var CalcPensionCeros= (PaseCalcPension - SumaDig);
return (CalcPensionCeros);
}
