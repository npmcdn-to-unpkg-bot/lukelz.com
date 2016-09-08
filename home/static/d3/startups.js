d3.select('#bar').attr('align', 'center');

const margin = {
  top: 20,
  right: 20,
  bottom: 30,
  left: 250,
};

const width = 800 - margin.left - margin.right;
const height = 800 - margin.top - margin.bottom;

// Scales
const x = d3.scale.linear()
  .range([0, width]);

const y = d3.scale.ordinal()
  .rangeRoundBands([0, height], 0.1);

// Axes
const xAxis = d3.svg.axis()
  .scale(x)
  .orient('top')
  .ticks(20);

const yAxis = d3.svg.axis()
  .scale(y)
  .orient('left');

// Create SVG element w/ margins and move it to the right
const svg = d3.select('body')
  .append('svg')
  .attr('width', width + margin.left + margin.right)
  .attr('height', height + margin.top + margin.bottom)
  .append('g')
  .attr('transform', `translate(${margin.left},${margin.top})`);

// Get json data and callback function
d3.json('/static/data/new_breakoutlist.json', (data) => {
  // create list of {name: , count: objects}

  let techData = [];
  let techDict = {};
  data.forEach((obj) => {
    const companyName = Object.keys(obj)[0];
    // console.log(company_name);
    const stack = obj[companyName].stack;
    //console.log(stack);
    for (techName in stack) {
      //console.log(techName);
      // console.log(stack[techName].category);
      if (techDict[techName]) {
        const techObj = techDict[techName];
        techObj.count += 1;
        // console.log(tech);
        // console.log(techObj.count);
      } else {
        const techObj = {
          name: techName,
          count: 1,
          category: stack[techName].category,
          root_category: stack[techName].root_category,
        }
        techData.push(techObj);
        techDict[techName] = techObj;
      }
    }
  });

  // Sort highest to lowest by count
  techData.sort((a, b) => b.count - a.count);
  techData = techData.splice(0, 28);

  // Get domains
  x.domain([0, d3.max(techData, (d) => d.count)]);
  y.domain(techData.map((d) => d.name));

  // Create x and y axes
  svg.append('g')
    .attr('class', 'x axis')
    .call(xAxis);

  svg.append('g')
    .attr('class', 'y axis')
    .call(yAxis);

  // Input data
  svg.selectAll('.bar')
    .data(techData)
    .enter()
    .append('rect') // x and y describe top left corner
    .attr('class', 'bar')
    .attr('x', 0)
    .attr('width', (d) => x(d.count))
    .attr('y', (d) => y(d.name))
    .attr('height', y.rangeBand());
});
