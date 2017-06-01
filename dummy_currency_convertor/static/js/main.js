var xhttp = new XMLHttpRequest();
var currencyBaseSymbol = 'EUR';
var curFromElement = document.getElementById("cur_from");
var curToElement = document.getElementById("cur_to");
var curTextElement = document.getElementById("cur_text");
var resultElement = document.getElementById("result");
var curAmount = document.getElementById("cur_amount");
var currencies;

curFromElement.onchange=function() {
    	loadCurrency('base='+this.value)
  	}

/*
    Implement function that fills currency from/to select boxes with currency codes
    and fills scrolling text with rates against currencyBaseSymbol
*/
function loadCurrency(attr='base='+currencyBaseSymbol) {
	xhttp.open("GET", "http://api.fixer.io/latest?"+attr, false);
	xhttp.send();
	var data = JSON.parse(xhttp.responseText);
	var option, i, rates= '';
	currencies = data.rates;
	curFromElement.options.length = 0;
	for (i in data.rates){
		addOption(curFromElement, i)
		addOption(curToElement, i)
         	rates += i + ": " + data.rates[i] + ", ";
	}
	addOption(curFromElement, data.base)
	addOption(curToElement, data.base)
	curFromElement.value = data.base
	curTextElement.innerHTML = 'BASE - ' + data.base + ' => ' + rates.slice(0, -1);
}

function addOption(target, opt) {
    	option = document.createElement("option");
	option.innerHTML = opt;
	target.appendChild(option);
}

/*
    Implement function that converts from one selected currency to another 
    filling result text area.
 */
function getRates() {
	from = curFromElement.value;
	to = curToElement.value;
	if (from === to) resultElement.value = "Enter another 'to' value";
	else resultElement.value = currencies[to] * curAmount.value;
}

// Load currency rates when page is loaded
window.onload = function() {
    (() => {loadCurrency(); setInterval(loadCurrency, 1000 * 60);})();
    var btn = document.getElementById('run');
    btn.addEventListener("click", getRates);
};
