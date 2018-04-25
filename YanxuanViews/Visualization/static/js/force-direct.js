function force_direct
{
            var img_w = 77;
            var img_h = 80;
            var radius = 15;  //圆形半径

            var svg = d3.select("svg"),
                width = +svg.attr("width"),
                height = +svg.attr("height");

            var color = d3.scaleOrdinal(d3.schemeCategory20);

            var simulation = d3.forceSimulation()
                .force("link", d3.forceLink().id(function(d) { return d.id; }))
                .force("charge", d3.forceManyBody())
                .force("center", d3.forceCenter(width / 2, height / 2));

            d3.json("../json/json_out.json", function(error, graph) 
                {
                  if (error) throw error;
                  var link = svg.append("g")
                      .attr("class", "links")
                    .selectAll("line")
                    .data(graph.links)
                    .enter().append("line")
                      .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

                  var node = svg.append("g")
                      .attr("class", "nodes")
                    .selectAll("circle")
                    .data(graph.nodes)
                    .enter().append("circle")
                      .attr("r", 5)
                      .attr("fill", function(d) { return color(d.group); })
                      .call(d3.drag()
                          .on("start", dragstarted)
                          .on("drag", dragged)
                          .on("end", dragended));

                  node.append("title")
                      .text(function(d) { return d.id; });

                  simulation
                      .nodes(graph.nodes)
                      .on("tick", ticked);

                  simulation.force("link")
                      .links(graph.links);

                  // 圆形图片节点（人物头像）
                  var nodes_img = svg.selectAll("image")
                                      .data(graph.nodes)
                                      .enter()
                                      .append("circle")
                                      .attr("class", "circleImg")
                                      .attr("r", radius)
                                      .attr("fill", function(d, i){

                                          //创建圆形图片
                                          var defs = svg.append("defs").attr("id", "imgdefs")

                                          var catpattern = defs.append("pattern")
                                                                  .attr("id", "catpattern" + i)
                                                                  .attr("height", 1)
                                                                  .attr("width", 1)

                                          catpattern.append("image")
                                                  .attr("x", - (img_w / 2 - radius))
                                                  .attr("y", - (img_h / 2 - radius))
                                                  .attr("width", img_w)
                                                  .attr("height", img_h)
                                                  .attr("xlink:href", d.image)

                                          return "url(#catpattern" + i + ")";

                                            }).call(d3.drag()
                                                    .on("start", dragstarted)
                                                    .on("drag", dragged)
                                                    .on("end", dragended));
                  function ticked() {
                    link
                        .attr("x1", function(d) { return d.source.x; })
                        .attr("y1", function(d) { return d.source.y; })
                        .attr("x2", function(d) { return d.target.x; })
                        .attr("y2", function(d) { return d.target.y; });

                    node
                        .attr("cx", function(d) { return d.x; })
                        .attr("cy", function(d) { return d.y; });

                    //更新结点图片和文字
                    nodes_img
                        .attr("cx",function(d){ return d.x })
                        .attr("cy",function(d){ return d.y });    
                        }
                });
            

            function dragstarted(d) {
              if (!d3.event.active) simulation.alphaTarget(0.3).restart();
              d.fx = d.x;
              d.fy = d.y;
            }

            function dragged(d) {
              d.fx = d3.event.x;
              d.fy = d3.event.y;
            }

            function dragended(d) {
              if (!d3.event.active) simulation.alphaTarget(0);
              d.fx = null;
              d.fy = null;
            }


