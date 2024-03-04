package main

import (
	"fmt"
	"net"
	"os"
	"reflect"
	"strconv"
	"strings"
)

var fileName string
var varStrings map[string]string
var varNums map[string]float64
var funcs map[string][]int
var lists map[string][]interface{}
var returnPositions []int
var lines []string
var terms [][]string
var messageLength int
var connection net.Conn
var buffer []byte
var pointer int = 0

const (
	serverHost = "localhost"
	serverPort = "6666"
	serverType = "tcp"
)

func checkIfVarOrList(term string) (interface{}, rune) {
	valueNum, ok := varNums[term]
	if ok {
		return valueNum, 'n'
	}
	valueString, ok := varStrings[term]
	if ok {
		return valueString, 's'
	}
	if strings.HasSuffix(term, ")") {
		var index int64
		index, err := strconv.ParseInt(term[strings.Index(term, "("):len(term)-1], 10, 64)
		if err != nil {
			panic(err)
		}
		valueType := reflect.ValueOf(lists[term[:strings.Index(term, "(")]][index]).Kind()
		switch reflect.ValueOf(valueType).Kind() {
		case reflect.Float64:
			valueFloat := lists[term[:strings.Index(term, "(")]][index].(float64)
			return valueFloat, 'n'
		case reflect.String:
			valueString := lists[term[:strings.Index(term, "(")]][index].(string)
			return valueString, 's'
		}
	}
	value, err := strconv.ParseFloat(term, 64)
	if err != nil {
		return term, 's'
	}
	return value, 'n'
}

func execute() {
	// for later buffer := make([]byte, 1024)
	// for later messageLength, err := connection.Read(buffer)
	connection, err := net.Dial(serverType, serverHost+":"+serverPort)
	if err != nil {
		panic(err)
	}

	_, err = connection.Write([]byte("connected"))
	if err != nil {
		panic(err)
	}

	if len(os.Args) < 2 {
		_, err = connection.Write([]byte("pexexit Keine Datei angegeben"))
	}
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		_, err = connection.Write([]byte("pexexit Datei kann nicht gelesen werden"))
	}
	fileName = os.Args[1]

	lines = strings.Split(string(data), "\r\n")
	for _, line := range lines {
		terms = append(terms, strings.Split(line, " "))
	}

	var currentTerm []string
	var isInVars []string
	for pointer < len(terms) {
		currentTerm = terms[pointer]
		_, okN := varNums[currentTerm[0]]
		_, okS := varStrings[currentTerm[0]]
		if okN {
			isInVars = append(isInVars, currentTerm[0], "n")
		} else if okS {
			isInVars = append(isInVars, currentTerm[0], "s")
		}

		switch currentTerm[0] {
		case "num":
			value, valueType := checkIfVarOrList(currentTerm[3])
			if valueType != 'n' {
				_, err = connection.Write([]byte("pexexit Wert ist keine Zahl"))
				if err != nil {
					panic(err)
				}
			}
			varNums[currentTerm[1]] = value.(float64)
			pointer++

		case "str":
			value, valueType := checkIfVarOrList(currentTerm[3])
			if valueType != 's' {
				_, err = connection.Write([]byte("pexexit Wert ist kein String"))
				if err != nil {
					panic(err)
				}
			}
			varStrings[currentTerm[1]] = value.(string)
			pointer++

		case "list":
			var values []interface{}
			for _, v := range currentTerm[3:] {
				value, err := strconv.ParseFloat(v, 64)
				if err != nil {
					values = append(values, v)
				}
				values = append(values, value)
			}
			lists[currentTerm[1]] = append(lists[currentTerm[1]], values)
			pointer++

		case "print":
			value, valueType := checkIfVarOrList(currentTerm[1])
			var text string
			switch valueType {
			case 's':
				text = "echo " + value.(string)
			case 'n':
				text = "echo " + fmt.Sprintf("%f", value.(float64))
			}
			_, err = connection.Write([]byte(text))
			if err != nil {
				panic(err)
			}
			pointer++

		case "if":
			value1, value1Type := checkIfVarOrList(currentTerm[1])
			value2, value2Type := checkIfVarOrList(currentTerm[3])

			switch currentTerm[2] {
			case "==":
				if value1 == value2 {
					pointer++
				} else {
					for terms[pointer][0] != "}" {
						pointer++
					}
					pointer++
				}
			case "!=":
				if value1 != value2 {
					pointer++
				} else {
					for terms[pointer][0] != "}" {
						pointer++
					}
					pointer++
				}
			case "<=":
				if value1Type != 'n' || value2Type != 'n' {
					_, err = connection.Write([]byte("pexexit <= ist nicht kompatibel mit String"))
					panic("exit")
				} else {
					if value1.(float64) <= value2.(float64) {
						pointer++
					} else {
						for terms[pointer][0] != "}" {
							pointer++
						}
						pointer++
					}
				}
			case ">=":
				if value1Type != 'n' || value2Type != 'n' {
					_, err = connection.Write([]byte("pexexit >= ist nicht kompatibel mit String"))
					panic("exit")
				} else {
					if value1.(float64) >= value2.(float64) {
						pointer++
					} else {
						for terms[pointer][0] != "}" {
							pointer++
						}
						pointer++
					}
				}
			case ">":
				if value1Type != 'n' || value2Type != 'n' {
					_, err = connection.Write([]byte("pexexit > ist nicht kompatibel mit String"))
					panic("exit")
				} else {
					if value1.(float64) > value2.(float64) {
						pointer++
					} else {
						for terms[pointer][0] != "}" {
							pointer++
						}
						pointer++
					}
				}
			case "<":
				if value1Type != 'n' || value2Type != 'n' {
					_, err = connection.Write([]byte("pexexit < ist nicht kompatibel mit String"))
					panic("exit")
				} else {
					if value1.(float64) < value2.(float64) {
						pointer++
					} else {
						for terms[pointer][0] != "}" {
							pointer++
						}
						pointer++
					}
				}
			default:
				_, err = connection.Write([]byte("pexexit Invalider Operator"))
				panic("exit")
			}

		case isInVars[0]:
			value, valueType := checkIfVarOrList(currentTerm[2])
			pointer++
			switch isInVars[1] {
			case "n":
				switch currentTerm[1] {
				case "=":
					if valueType == 'n' {
						varNums[currentTerm[0]] = value.(float64)
					} else {
						_, err = connection.Write([]byte("pexexit Num Variable kann nicht mit String belegt werden"))
						panic("exit")
					}
				case "+=":
					if valueType == 'n' {
						varNums[currentTerm[0]] += value.(float64)
					} else {
						_, err = connection.Write([]byte("pexexit Num Variable kann nicht mit String addiert werden"))
						panic("exit")
					}
				case "-=":
					if valueType == 'n' {
						varNums[currentTerm[0]] -= value.(float64)
					} else {
						_, err = connection.Write([]byte("pexexit Num Variable kann nicht mit String subtrahiert werden"))
						panic("exit")
					}
				case "*=":
					if valueType == 'n' {
						varNums[currentTerm[0]] *= value.(float64)
					} else {
						_, err = connection.Write([]byte("pexexit Num Variable kann nicht mit String multipliziert werden"))
						panic("exit")
					}
				case "/=":
					if valueType == 'n' {
						varNums[currentTerm[0]] /= value.(float64)
					} else {
						_, err = connection.Write([]byte("pexexit Num Variable kann nicht mit String dividiert werden"))
						panic("exit")
					}
				default:
					_, err = connection.Write([]byte("pexexit Invalider Operator"))
					panic("exit")
				}
			case "s":
				switch currentTerm[1] {
				case "=":
					if valueType == 's' {
						varStrings[currentTerm[0]] = value.(string)
					} else {
						_, err = connection.Write([]byte("pexexit String kann nicht mit Num gleichgesetzt werden"))
						panic("exit")
					}
				default:
					_, err = connection.Write([]byte("pexexit Invalider Operator"))
					panic("exit")
				}
			}
		default:
			_, err = connection.Write([]byte("pass"))
			if err != nil {
				panic(err)
			}
			pointer++
		}

	}
	_, err = connection.Write([]byte("pexexit Programm beendet"))
	if err != nil {
		panic(err)
	}
}

func main() {
	varNums = make(map[string]float64)
	varStrings = make(map[string]string)
	lists = make(map[string][]interface{})
	funcs = make(map[string][]int)

	execute()
}
