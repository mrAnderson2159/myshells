const fs = require('fs');
const scanf = require('scanf');
const { execSync } = require('child_process');

const dbPath = `${__dirname}/database.json`
let dbParsed = JSON.parse(fs.readFileSync(dbPath, 'utf8'))
const pargv = process.argv.slice(2)


let { turni, zoolab } = dbParsed
let answer

switch (pargv[0]) {
    case '--edit':
        execSync(`atom ${__filename}`)
        break;
    case '-i':
        console.log(info());
        break;
    case '-t':
        turnMenu()
        break;
    case '-z':
        zoolabMenu()
        break;
    default:
        throw 'exeption: flag sconosciuta\n' + info()
}




// Turni

function info() {
    let s = 'utilizzo: ffx [-itz | --edit]\n'
    s += '\n\t--edit: modalità sviluppo codice\n\n'
    s += '\t-i: info\n'
    s += '\t-t: menù turnazione\n'
    s += '\t-z: menù zoolab\n'
    return s
}

function errCondition(condition, err, callback = () => '') {
    if (condition) {
        console.log(err);
        callback()
    }
}

function turnMenu() {
    console.log("I personaggi attivi al momento sono");
    printCharacters()
    console.log('\nDesideri modificare questa lista? (y/n)');
    do {
        answer = scanf('%s')
        errCondition(answer !== 'y' && answer !== 'n', 'Scelta non corretta.\nDesideri modificare questa lista? (y/n)')
    } while (answer !== 'y' && answer !== 'n');
    modifyList(answer)
    turnGame()
}

function toggleCharacter(longevity) {
    console.log("Quale personaggio vuoi attivare o disattivare?");
    do {
        answer = scanf('%s')
        errCondition(!(answer in turni), `${answer} non è un personaggio, Quale personaggio vuoi attivare o disattivare?`)
    } while (!(answer in turni));
    turni[answer] = !turni[answer]
    if (longevity === 'p') fs.writeFileSync(dbPath, JSON.stringify(dbParsed))
    if (turni[answer])
        console.log(`${answer} è stato attivato ${longevity === 'p' ? 'permanente':''}`);
    else
        console.log(`${answer} è stato disattivato ${longevity === 'p' ? 'permanente':''}`);
}

function modifyList(answer) {
    if (answer === 'y') {
        console.log('Desideri modificarla permanente (p) o solo per questa volta (o)?');
        do {
            answer = scanf('%s')
            errCondition(answer !== 'p' && answer !== 'o', 'Scelta non corretta.\nDesideri modificarla permanente (p) o solo per questa volta (o)?')
        } while (answer !== 'p' && answer !== 'o');
        do {
            if (answer === 'p')
                toggleCharacter(answer)
            else
                toggleCharacter(answer)
            console.log('Vuoi modificare nuovamente la lista? (y/n)');
            answer = scanf('%s')
            errCondition(answer !== 'y' && answer !== 'n', 'Scelta non corretta.\nVuoi modificare nuovamente la lista? (y/n)')
        } while (answer !== 'y' && answer !== 'n');
        if (answer === 'y')
            modifyList('y')
    }
}

function printCharacters() {
    let count = 0
    for (let character in turni)
        if (turni[character])
            console.log(`${++count}. ${character}`);
}

function charInit() {
    let string = ''
    for (let character in turni)
        if (turni[character])
            string += `${character[0]}`
    string.substring(0, string.length - 3)
    return string.split('').sort().join(', ')
}

function errCharCondition(answer) {
    let chars = charInit().split(', ')
    return (function innerRecursive(length) {
        if (length === 0) return true
        return answer !== chars[--length] && innerRecursive(length)
    }(chars.length))
}

function toggleCharacterInit(char) {
    for (let character in turni)
        if (new RegExp(`^${char}`, 'i').test(character)) {
            turni[character] = !turni[character]
            break
        }
}

function nextTurn() {
    console.log('Devono ancora giocare:');
    printCharacters()
    console.log(`\nChi ha appena giocato? (${charInit()})`);
    do {
        answer = scanf('%s')
        errCondition(errCharCondition(answer), `${answer} non corrisponde a un personaggio,\nChi ha appena giocato? (${charInit()})`)
    } while (errCharCondition(answer));
    toggleCharacterInit(answer)
}

function turnGame() {
    turni = JSON.parse(fs.readFileSync(dbPath, 'utf8')).turni
    console.log('\nCominciamo la partita!\n');
    do {
        nextTurn()
    } while (charInit());
    console.log('\nNuova partita? (y/n)');
    do {
        answer = scanf('%s')
        errCondition(answer !== 'y' && answer !== 'n', 'Scelta non corretta.\nVuoi iniziare una nuova partita? (y/n)')
    } while (answer !== 'y' && answer !== 'n');
    if (answer === 'y')
        turnGame()
}




// Zoolab

function zoolabMenu() {
    console.clear()
    console.log('Benvenuto nella sezione zoolab! A quale categoria vuoi accedere?');
    zMainMenu()
}

function enter() {
    scanf('%d')
}

function cap(string) {
    if (!string) return ''
    let newString
    if (/\W/g.test(string)) {
        const nonWords = string.match(/\W/g)
        string = /\?/.test(string) ? string[0].toUpperCase() + string.slice(1) : string.split(/\W/g).map(x => x[0].toUpperCase() + x.substr(1))
        newString = string[0]
        for (let i = 0; i < nonWords.length; i++) newString += nonWords[i] + string[i + 1]
    } else
        newString = string[0].toUpperCase() + string.slice(1)
    return newString
}

function zoneFromFiend(fiend, res = 'str') {
    fiend = cap(fiend)
    for (let zone in zoolab.bestiario) {
        let thisZone = zoolab.bestiario[zone]
        if (fiend in thisZone) {
            if (res === 'obj') return zoolab.bestiario[zone]
            else if (res === 'str') return zone
        }
    }
}

function checkZoneChampionReady(zone) {
    zone = cap(zone)
    let champion;
    for (let champ in zoolab['Campioni Di Zona']) {
        if (zoolab['Campioni Di Zona'][champ].zoneRequired === zone) {
            champion = zoolab['Campioni Di Zona'][champ]
            break
        }
    }

    if (champion.exist) return

    for (let fiend in zoolab.bestiario[zone])
        if (!zoolab.bestiario[zone][fiend].wasCaptured) return

    champion.exist = true

    console.clear()
    console.log(`Congratulazioni! \n\n${champion.name} è appena stato creato nei Campioni di Zona!\n`);
    console.log(`Ricompensa: ${champion.reward}`);
    enter()
}

function checkKindChampionReady(fiend) {
    fiend = cap(fiend)
    let champion
    for (let zone in zoolab.bestiario) {
        let thisZone = zoolab.bestiario[zone]
        if (fiend in thisZone) {
            if (!thisZone[fiend].createsChampion) return
            champion = thisZone[fiend].createsChampion
            fiend = ''
            break
        } else return
    }
    champion = zoolab['Campioni Di Specie'][champion]

    if (champion.exist) return

    for (fiend of champion.kindRequired.fiends)
        if (zoneFromFiend(fiend, 'obj')[fiend].wasCaptured < champion.kindRequired.quantity) return

    champion.exist = true

    console.clear()
    console.log(`Congratulazioni! \n\n${champion.name} è appena stato creato nei Campioni di Specie!\n`);
    console.log(`Ricompensa: ${champion.reward}`);
    enter()
}

function checkPrototypeReady() {
    let prototype, count, exist = false
    for (let proto in zoolab['Prototipi Zoolab']) {
        console.log(proto);
        if (exist) break
        prototype = zoolab['Prototipi Zoolab'][proto]
        if (prototype.exist) continue
        switch (proto) {
            case 'Mangiaterra':
                count = 0
                for (let fiend in zoolab["Campioni Di Zona"]) {
                    if (zoolab["Campioni Di Zona"][fiend].exist)
                        ++count
                    if (count === 2) {
                        exist = true
                        break
                    }
                }
                break;
            case 'Titanosfera':
                count = 0
                for (let fiend in zoolab["Campioni Di Specie"]) {
                    if (zoolab["Campioni Di Specie"][fiend].exist)
                        ++count
                    if (count === 2) {
                        exist = true
                        break
                    }
                }
                break;
            case 'Catastrophe':
                count = 0
                for (let fiend in zoolab["Campioni Di Zona"]) {
                    if (zoolab["Campioni Di Zona"][fiend].exist)
                        ++count
                    if (count === 6) {
                        exist = true
                        break
                    }
                }
                break;
            case 'Vlakorados':
                count = 0
                for (let fiend in zoolab["Campioni Di Specie"]) {
                    if (zoolab["Campioni Di Specie"][fiend].exist)
                        ++count
                    if (count === 6) {
                        exist = true
                        break
                    }
                }
                break;
            case 'Gasteropodos':
                exist = true
                for (let zone in zoolab.bestiario) {
                    if (!exist) break
                    if (zone === 'Others') continue
                    for (let fiend in zoolab.bestiario[zone]) {
                        process.stdout.write(`\n${fiend}`)
                        if (!(zoolab.bestiario[zone][fiend].wasCaptured)) {
                            exist = false
                            break
                        }
                    }
                }
                break;
            case 'Ultima X':
                exist = true
                for (let zone in zoolab.bestiario) {
                    if (!exist) break
                    if (zone === 'Others') continue
                    for (let fiend in zoolab.bestiario[zone])
                        if ((zoolab.bestiario[zone][fiend].wasCaptured) < 5) {
                            exist = false
                            break
                        }
                }
                break;
            case 'Shinryu':
                const gagazet = zoolab.bestiario['Monte Gagazet']
                if (gagazet.Splasher.wasCaptured === 2 && gagazet.Aquelous.wasCaptured === 2 && gagazet.Echeneis.wasCaptured === 2)
                    exist = true
                break;
            case 'Il Supremo':
                exist = true
                const champTypes = ['Campioni Di Zona', 'Campioni Di Specie', 'Prototipi Zoolab']
                for (type of champTypes)
                    for (let champion in zoolab[type]) {
                        if (champion === 'Il Supremo')
                            continue
                        if (!zoolab[type][champion].exist || !zoolab[type][champion].wasDefeated) {
                            exist = false
                            break
                        }
                    }
        }
    }
    if (!exist) return
    prototype.exist = true
    console.clear()
    console.log(`Congratulazioni! \n\n${prototype.name} è appena stato creato nei Prototipi Zoolab!\n`);
    console.log(`Ricompensa: ${prototype.reward}`);
    enter()

}

function missingFiends(champion) {
    const champTypes = ['Campioni Di Zona', 'Campioni Di Specie', 'Prototipi Zoolab']
    for (type of champTypes) {
        if (champion in zoolab[type]) {
            champion = zoolab[type][champion]
            switch (type) {
                case 'Campioni Di Zona':
                    const zoneRequired = champion.zoneRequired
                    const remaining = []
                    for (let fiend in zoolab.bestiario[zoneRequired]) {
                        if (!zoolab.bestiario[zoneRequired][fiend].wasCaptured) {
                            remaining.push(fiend)
                        }
                    }
                    return remaining
                    break;
                case 'Campioni Di Specie':
                    const kindRequired = champion.kindRequired.fiends
                    const quantity = champion.kindRequired.quantity
                    const fiends = []
                    const result = {}
                    for (fiend of kindRequired) {
                        for (let zone in zoolab.bestiario) {
                            if (fiend in zoolab.bestiario[zone]) {
                                fiends.push(zoolab.bestiario[zone][fiend])
                            }
                        }
                    }
                    for (fiend of fiends) {
                        if (fiend.wasCaptured < quantity) {
                            result[fiend] = quantity - fiend.wasCaptured
                        }
                    }
                    return result
                    break;
                case 'Prototipi Zoolab':

                    break;
                default:

            }
        }
    }

}

function zMainMenu() {

    console.log('\t1. Battuta di caccia\n\t2. Quadro generale cattura\n\t3. Bestiario\n\t4. Tangente');
    const choice = scanf('%d')
    switch (choice) {
        case 1:
            battutaDiCaccia()
            break;
        case 2:
            quadroGenerale()
            break;
        case 3:
            bestiario()
            break;
        case 4:
            tangente()
            break;
        default:
            console.log("Scelta sbagliata");
            setTimeout(() => {
                console.clear()
                zMainMenu()
            }, 1000)
    }
}

function battutaDiCaccia() {
    console.clear()
    let count = 0
    let choice
    let zones = []
    do {
        count = logZones(true).count
        zones = logZones().array
        choice = scanf('%d')
        console.clear()
        errCondition(choice < 1 || choice > count, 'Scelta sbagliata\n')
    } while (choice < 1 || choice > count);
    fiendHunt(choice, zones)

}

function quadroGenerale() {
    let content = 'Hai catturato\n'
    let selectedZone
    for (let zone in zoolab.bestiario) {
        selectedZone = zoolab.bestiario[zone]
        content += `\n\n${zone}\n\n`
        if (zone === 'Others') continue
        for (let fiend in selectedZone) {
            if (fiend === 'isNeeded') continue
            content += `${fiend}:${fiend.length > 14 ? '\t\t':(fiend.length < 7 ? '\t\t\t\t':'\t\t\t')}${selectedZone[fiend].wasCaptured}`
            content += zoolab['Campioni Di Specie'][selectedZone[fiend].createsChampion] ? `${selectedZone[fiend].wasCaptured === zoolab['Campioni Di Specie'][selectedZone[fiend].createsChampion].kindRequired.quantity ? ' *':''}\n` : '\n'
        }
    }
    content += '\nHai creato\n'
    const champTypes = ['Campioni Di Zona', 'Campioni Di Specie', 'Prototipi Zoolab']
    for (type of champTypes) {
        content += `\n${type}\n\n`
        for (let champion in zoolab[type]) {
            if (zoolab[type][champion].exist)
                content += `${champion}\n`
            else {
                switch (type) {
                    case 'Campioni Di Zona':

                        break;
                    case 'Campioni Di Specie':

                        break;
                    case 'Prototipi Zoolab':

                        break;
                    default:

                }
            }
        }
    }
    fs.writeFileSync(`/Users/mr.anderson2159/Desktop/Resoconto Zoolab.txt`, content)
    execSync('open ~/Desktop/Resoconto\\ Zoolab.txt')
    zoolabMenu()
}

function bestiario() {

}

function tangente() {

}

function logZones(log = false) {
    if (log) console.log("Seleziona una zona");
    let count = 0
    const array = []
    for (let zone in zoolab.bestiario) {
        if (zoolab.bestiario[zone].isNeeded) {
            zoolab.bestiario[zone].isNeeded = false
            for (let fiend in zoolab.bestiario[zone]) {
                if (zoolab.bestiario[zone][fiend].capturable && zoolab.bestiario[zone][fiend].wasCaptured !== 10) {
                    zoolab.bestiario[zone].isNeeded = true
                    break
                }
            }
        }
    }

    for (let zone in zoolab.bestiario)
        if (zoolab.bestiario[zone].isNeeded) {
            array.push(zone)
            if (log) console.log(`${++count}. ${zone}`);
        }
    return {
        array,
        count
    }
}

function printZoneFiends(choice, zones, log = false) {
    const selectedZoneName = zones[choice - 1]
    const selectedZone = zoolab.bestiario[selectedZoneName]
    let count = 0
    let scanfString = ''
    let choice2
    const array = []
    if (log) console.log(`Ecco i mostri che devi catturare nella zona "${selectedZoneName}" e quanti ne hai catturati:\n`);
    for (let fiend in selectedZone)
        if (selectedZone[fiend].isNeeded) {
            array.push(fiend)
            if (log)
                console.log(`${++count}. ${fiend}:${fiend.length > 11 ? '\t\t':(fiend.length < 4 ? '\t\t\t\t':'\t\t\t')}${selectedZone[fiend].wasCaptured}${zoolab['Campioni Di Specie'][selectedZone[fiend].createsChampion] ? (selectedZone[fiend].wasCaptured >= zoolab['Campioni Di Specie'][selectedZone[fiend].createsChampion].kindRequired.quantity ? ' *':''):''}`)
        }
    if (log) {
        console.log('\nQuanti mostri hai appena catturato?\n');
        choice2 = scanf('%d')
        if (choice2) {
            for (let i = 0; i < choice2; i++)
                scanfString += '%d'
            console.log(choice2 === 1 ? `\nInserisci l'indice del mostro catturato\n` : `\nInserisci gli indici dei ${choice2} mostri catturati\n`);
        } else {
            console.log('\nPare che tu non abbia catturato mostri, desideri cambiare zona? (Y/n)');
            choice2 = scanf('%s')
            switch (choice2) {
                case 'y':
                    battutaDiCaccia()
                    break;
                case 'n':
                    console.clear()
                    fiendHunt(choice, zones)
            }
        }
    }
    return {
        remainedFiends: array,
        count,
        scanfString,
        selectedZoneName,
        selectedZone
    }
}

function fiendHunt(choice, zones) {
    let capturedFiends = []
    let choice2
    let { count, remainedFiends, scanfString, selectedZone, selectedZoneName } = printZoneFiends(choice, zones, true)
    capturedFiends = scanf(scanfString)
    capturedFiends = typeof capturedFiends === 'object' ? capturedFiends.map(x => remainedFiends[x - 1]) : [remainedFiends[capturedFiends - 1]]
    console.clear()
    console.log(`Confermi di aver catturato ${niceJoinArray(capturedFiends)} (Y/n)?\n`);
    choice2 = scanf('%s')
    switch (choice2) {
        case 'y':
            updateZoolab({ capturedFiends, selectedZone, selectedZoneName, hunt: true })
            fiendHunt(choice, zones)
            break;
        case 'n':
            console.clear()
            fiendHunt(choice, zones)
    }
}

function niceJoinArray(array) {
    let temp = []
    for (let i = 0; i < array.length; i++) {
        temp[i] = array[i]
    }
    if (temp.length) {
        for (let i = 0; i < temp.length; i++) {
            if (temp.length === 1) {
                temp = temp[0]
                break
            }
            if (temp.length === 2) {
                temp = temp.join(' e ')
                break
            }
            if (i < temp.length - 2) {
                temp[i] += ', '
            } else if (i === temp.length - 2) {
                temp[i] += ' e '
            } else break
        }
        if (typeof temp === 'object')
            temp = temp.join('')
        return temp
    }
}

function updateZoolab({ capturedFiends, selectedZone, selectedZoneName, hunt = false }) {
    if (hunt) {
        for (fiend of capturedFiends) {
            selectedZone[fiend].wasCaptured++
            if (selectedZone[fiend].wasCaptured === 10)
                selectedZone[fiend].isNeeded = false
            checkKindChampionReady(fiend)
        }
        checkZoneChampionReady(selectedZoneName)
        checkPrototypeReady()
    }
    fs.writeFileSync(dbPath, JSON.stringify(dbParsed))
    console.clear()
}
