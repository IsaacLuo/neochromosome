var fnNeoChromosomeTRNASearch = function (node) {   
	node.addField("ID", "String", "");
	node.addField("Status", "String", "");
	node.addField("Seq5", "Undefined", "");
	node.addField("Seq3", "Undefined", "");

    pyCode = "import neochromosome\nresult = neochromosome.checkTRNA(self.ID)\nself.Status=result['Statues']\nself.Seq5=result['Seq5']\nself.Seq3=result['Seq3']\n";
    node.setPythonCompute(pyCode);
};

var fnNeoChromosomeTRNAMatch = function (node) {   
	node.addField("ID", "String", "");
	node.addField("Seq5", "Undefined", "");
	node.addField("Seq3", "Undefined", "");
	node.addField("Result", "String", "");

    pyCode = "import neochromosome\nresult = neochromosome.matchTRNA(self.ID,self.Seq5,self.Seq3)\nself.Result=result['Result']\n";
    node.setPythonCompute(pyCode);
};

var fnNeoChromosomeTRNAAppend = function (node) {   
	node.addField("ID", "String", "");
	node.addField("Seq5", "Undefined", "");
	node.addField("Seq3", "Undefined", "");
	node.addField("Result", "String", "");

    pyCode = "import neochromosome\nresult = neochromosome.appendTRNA(self.ID,self.Seq5,selfSeq3)\nself.Result=result['Result']\n";
    node.setPythonCompute(pyCode);
};

defineNodeType('Main','Search',fnTest);

createCassette('Main');

addCassetteItem('Neochromosome', 'Main.Search','https://cyborg.autodesk.com/siteversion/cyborg/res/cassettes/action-icons/Cube.png';

