set = {"LoremIpsum LoremIpsum" : ["Ans1", "Ans2", "Ans3", "Ans3"], Sample2: ["Ans2", "Ans3", "Ans4", "Ans5"], SampleQA: ["Ans1", "Ans2", "Ans3", "Ans3"], Sample22: ["Ans2", "Ans3", "Ans4", "Ans5"], SampleQS: ["Ans1", "Ans2", "Ans3", "Ans3"], Sample24: ["Ans2", "Ans3", "Ans4", "Ans5"]}
listy = document.getElementById("questionList")
mother = document.getElementById("mother")
count=1
var activeQ=0;
var activeN=1;
switchQuestion = function(qNo){
    prevButt = document.getElementById("prev")
    nextButt = document.getElementById("next")
    if (qNo<=Object.keys(set).length&&qNo>=1)
    {q = document.getElementById("q"+qNo)
    activeQ.style.display = "none"
    q.style.display="block"
    activeQ = q
    activeN = qNo}
    if(qNo==1){
        prevButt.style.display="none"
        nextButt.style.display="inline"
    } else if(qNo==Object.keys(set).length){
        nextButt.style.display="none"
        prevButt.style.display = "inline"
    } else {
        nextButt.style.display="inline"
        prevButt.style.display = "inline"
    }
}
questionClick = function(data){
    switchQuestion(data.target.value)
    console.log(set.length)
}

for (var j in set){
    li = document.createElement("li")
    li.classList = "nos"
    li.innerHTML = count
    li.onclick = questionClick
    li.value=count
    listy.appendChild(li)
    mC = document.createElement("div")
    mC.id = "q"+count
    mC.innerHTML = `<h2>QUESTION ${count}</h2>
    <div class="question">
        <p>${j}</p>
        <form>
            <label><input type="radio" name="answer"> ${set[j][0]}</label><br>
            <label><input type="radio" name="answer"> ${set[j][1]}</label><br>
            <label><input type="radio" name="answer" checked> ${set[j][2]}</label><br>
            <label><input type="radio" name="answer"> ${set[j][3]}</label>
        </form>
    </div>`
    if(count!=1){
        mC.style.display = "none"
    }
    activeQ = document.getElementById("q1")
    mother.appendChild(mC)
    count++
}
