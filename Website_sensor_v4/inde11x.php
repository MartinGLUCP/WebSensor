<?php
session_start();
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <title>Accueil</title>
    <meta charset="UTF-8">
  	<meta http-equiv="X-UA-Compatible" content="IE=edge">
  	<meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="css/style2.css">    
</head>
<body>
<?php
	require ('include/header.inc.php');
	headWeb("Index","Gestion de l'apprentissage","home","index");
?>
<div class ="img-header">
  <img id="logo" src="img/tweeter.jpg" alt="accueil">
</div>

  </div>
<section class="main">

<div class="searchbar">
                               
    <div class="navbar-form collapse navbar-collapse">
       <form class="pieform header-search-form" name="usf" method="post" action="index.php" id="usf">
      <div><span id="usf_query_container" class="form-group-inline">
        <label class="sr-only" for="usf_query">Search</label>
  <input type="text" class="form-control text" id="usf_query" name="query" placeholder="Search" tabindex="0" value=""></span>
  <span id="usf_submit_container" class="form-group-inline">
    <button type="submit"  class="btn-default input-group-btn button btn" id="usf_submit" name="submit" tabindex="0">
      <span class="icon icon-search icon-lg" role="presentation" aria-hidden="true"></span><span class="sr-only">Goooooo</span>
    </button></span></div><input type="hidden" class="hidden" id="usf_sesskey" name="sesskey" value="">
<input type="hidden" name="pieform_usf" value="ff">
        </form>

        </div>
    </div>
	
</section>

<script src="https://d3js.org/d3.v4.min.js"></script>

<?php
  require ('include/header.inc.php');
  
  $connexion = new PDO('pgsql:host=postgresql-websensor.alwaysdata.net;port=5432;dbname=websensor_2019;user=websensor;password=projet2019');
  $resultset = $connexion->prepare("SELECT * FROM vectors");
  $resultset->execute();
  $count = $resultset->rowCount();
  while ($row = $resultset->fetch(PDO::FETCH_ASSOC)) {
    print(strval($row["vector"]));
    print(strval($row["tweet_content"]));
    print(strval($row["id_tweet"]));
    print(strval($row["date"]));
  }
  print($count);
  
?>
<section id="main">
  <div id="container">
  </div>
</section>


<!-------------------------------- GRAPHIQUE D3JS ----------------------------------------------------->

<script>

data = [{
  "donnee" : 10,
  "donnee2" : 12,
  "date" : "17-Apr-2020"
},
{
  "donnee" : 11,
  "donnee2" : 12,
  "date" : "11-May-2020"
},
{
  "donnee" : 18,
  "donnee2" : 9,
  "date" : "12-Jun-2020"
},
{
  "donnee" : 16,
  "donnee2" : 7,
  "date" : "13-Feb-2020"
},
{
  "donnee" : 15,
  "donnee2" : 5,
  "date" : "14-Jan-2020"
},
{
  "donnee" : 11,
  "donnee2" : 4,
  "date" : "15-Dec-2020"
},
{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "01-Jan-2020"
},
{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "01-Feb-2020"
},
{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "01-Mar-2020"
},
{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "01-Apr-2020"
},{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "01-May-2020"
},{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "10-Jun-2020"
},{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "16-Jul-2020"
},{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "01-Aug-2020"
},
{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "01-Sep-2020"
},
{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "01-Oct-2020"
},
{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "01-Nov-2020"
},
{
  "donnee" : 0,
  "donnee2" : 0,
  "date" : "01-Dec-2020"
},
]

console.log(data)

// set the dimensions and margins of the graph
var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// parse the date / time
var parseTime = d3.timeParse("%d-%b-%Y");

// set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

// define the 1st line
var valueline = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.close); });

// define the 2nd line
var valueline2 = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.open); });

// append the svg obgect to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// format the data
data.forEach(function(d) {
  d.date = parseTime(d.date);
  d.close = +d.donnee;
  d.open = +d.donnee2;
});

data.sort(function(a, b) {
    return a.date - b.date;
});
  
// Scale the range of the data
x.domain(d3.extent(data, function(d) { return d.date; }));
y.domain([0, d3.max(data, function(d) {
  return Math.max(d.close, d.open); })]);

// Add the valueline path.
svg.append("path")
  .data([data])
  .attr("class", "line")
  .style("stroke", "red")
  .attr("d", valueline);

// Add the valueline2 path.
svg.append("path")
  .data([data])
  .attr("class", "line")
  .style("stroke", "blue")
  .attr("d", valueline2);
  
// Add the X Axis
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x));

// Add the Y Axis
svg.append("g")
  .call(d3.axisLeft(y));


/*
//Initialisation

const margin = {top: 50, right: 30, bottom: 30, left: 60},
    width = 500;//document.getElementById("container").offsetWidth * 0.95 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

const parseTime = d3.timeParse("%d/%m/%Y");
const dateFormat = d3.timeFormat("%d/%m/%Y");

const x = d3.scaleTime()
    .range([0, width]);

const y = d3.scaleLinear()
    .range([height, 0]);
    
const line = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.close); });

const area = d3.area()
    .x(function(d) { return x(d.date); })
    .y0(height)
    .y1(function(d) { return y(d.close); });

// Attention ici il faut que le body possède déjà un DIV dont l'ID est chart
const svg = d3.select("#container").append("svg")
    .attr("id", "svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//Ajout d'un titre  
svg.append("text")
    .attr("x", (width / 2))             
    .attr("y", 0 - (margin.top / 2))
    .attr("text-anchor", "middle")
    .style("fill", "#5a5a5a")
    .style("font-family", "Raleway")
    .style("font-weight", "300")
    .style("font-size", "24px")
    .text("Cours journalier de l'or depuis 2001");

//  Ajout du tooltip
function addTooltip() {
    // Création d'un groupe qui contiendra tout le tooltip plus le cercle de suivi
    var tooltip = svg.append("g")
        .attr("id", "tooltip")
        .style("display", "none");
    
    // Le cercle extérieur bleu clair
    tooltip.append("circle")
        .attr("fill", "#CCE5F6")
        .attr("r", 10);

    // Le cercle intérieur bleu foncé
    tooltip.append("circle")
        .attr("fill", "#3498db")
        .attr("stroke", "#fff")
        .attr("stroke-width", "1.5px")
        .attr("r", 4);
    
    // Le tooltip en lui-même avec sa pointe vers le bas
    // Il faut le dimensionner en fonction du contenu
    tooltip.append("polyline")
        .attr("points","0,0 0,40 55,40 60,45 65,40 120,40 120,0 0,0")
        .style("fill", "#fafafa")
        .style("stroke","#3498db")
        .style("opacity","0.9")
        .style("stroke-width","1")
        .attr("transform", "translate(-60, -55)");
    
    // Cet élément contiendra tout notre texte
    var text = tooltip.append("text")
        .style("font-size", "13px")
        .style("font-family", "Segoe UI")
        .style("color", "#333333")
        .style("fill", "#333333")
        .attr("transform", "translate(-50, -40)");
    
    // Element pour la date avec positionnement spécifique
    text.append("tspan")
        .attr("dx", "-5")
        .attr("id", "tooltip-date");
    
    // Positionnement spécifique pour le petit rond bleu
    text.append("tspan")
        .style("fill", "#3498db")
        .attr("dx", "-60")
        .attr("dy", "15")
        .text("●");

    // Le texte "Cours : "
    text.append("tspan")
        .attr("dx", "5")
        .text("Cours : ");
    
    // Le texte pour la valeur de l'or à la date sélectionnée
    text.append("tspan")
        .attr("id", "tooltip-close")
        .style("font-weight", "bold");
    
    return tooltip;
}

// Création des axes et de la ligne
 
d3.tsv("data.tsv", function(error, data) {
    data.forEach(function(d) {
        d.date = parseTime(d.date);
        d.close = +d.close;
    });
    
    data.sort(function(a, b) {
        return a.date - b.date;
    });
    

    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain(d3.extent(data, function(d) { return d.close; }));
  
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    svg.append("g")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("fill", "#000")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", "0.71em")
        .style("text-anchor", "end")
        .text("");//AFAIRE nom de la donnée de l'axe y
  
    svg.selectAll("y axis").data(y.ticks(10)).enter()
        .append("line")
        .attr("class", "horizontalGrid")
        .attr("x1", 0)
        .attr("x2", width)
        .attr("y1", function(d){ return y(d);})
        .attr("y2", function(d){ return y(d);});
        
    var linePath = svg.append("path")
        .datum(data)
        .style("fill", "none")
        .style("stroke", "#3498db")
        .style("stroke-width", "1px")
        .style("opacity", "0.6")
        .attr("d", line);
    
    // dégradé sous la courbe (Area Chart)

  svg.append("linearGradient")
    .attr("id", "areachart-gradient")
    .attr("gradientUnits", "userSpaceOnUse")
    .attr("x1", 0)
    .attr("x2", 0)
    .attr("y1", y(d3.min(data, function(d) { return d.close; })))
    .attr("y2", y(d3.max(data, function(d) { return d.close; })))
    .selectAll("stop")
      .data([
        {offset: "0%", color: "#F7FBFE"},
        {offset: "100%", color: "#3498DB"}
      ])
    .enter().append("stop")
      .attr("offset", function(d) { return d.offset; })
      .attr("stop-color", function(d) { return d.color; });
      
  var areaPath = svg.append("path")
    .datum(data)
    .style("fill", "url(#areachart-gradient)")
    .style("opacity", "0.6")
    .attr("d", area);
    
  // Gestion des évènements de la souris

  var tooltip = addTooltip();

  var bisectDate = d3.bisector(function(d) { return d.date; }).left;

  svg.append("rect")
    .attr("class", "overlay")
    .attr("width", width)
    .attr("height", height)
    .attr("opacity",0)
    .on("mouseover", function() { 
      tooltip.style("display", null);
    })
    .on("mouseout", function() {
      tooltip.style("display", "none");
    })
    .on("mousemove", mousemove);
    
  function mousemove() {
    var x0 = x.invert(d3.mouse(this)[0]),
      i = bisectDate(data, x0),
      d = data[i];
    
    tooltip.attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")");
    
    d3.select('#tooltip-date')
      .text(dateFormat(d.date));
    d3.select('#tooltip-close')
      .text(d.close + "$");
  }
  
});
*/
</script>

<!------------------------------------------------------------------------------------------------->


<footer id="footer">
          <p>Copyright Andreas, &copy; 2019</p>
          <p>Reproduction interdite</p>
</footer>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="js/bootstrap.min.js"></script>
</body>
</html>


<footer id="footer">
          <p>Copyright Web Sensor, &copy; 2020</p>
          <p>Reproduction interdite</p>
</footer>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="js/bootstrap.min.js"></script>
</body>
</html>
