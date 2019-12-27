function genRandomInt(max) {
    return 1 + Math.floor(Math.random() * Math.floor(max+1));
}
function genRandomArray(realArrays, max, privacyThreshold=0.5){
    let rand = Math.random();
    let genArrays = realArrays.map(d=>d);
    console.log(rand);
    if(rand > privacyThreshold){
        let newGen = genRandomInt(max);
        genArrays[genArrays.length - 1] = newGen;
    }
    return genArrays;
}

export default genRandomArray;