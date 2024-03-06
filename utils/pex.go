package main

import (
	"fmt"
	"math/rand/v2"
	"os"
	"reflect"
	"slices"
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
var pointer int = 0

func deleteElement(slice []int, index int) []int {
	return append(slice[:index], slice[index+1:]...)
}

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
		var float float64
		value, _ := checkIfVarOrList(term[strings.Index(term, "(")+1 : len(term)-1])
		index = int64(value.(float64))
		valueAtIndex := lists[term[:strings.Index(term, "(")]][index]
		valueType := reflect.TypeOf(valueAtIndex)
		if valueType != reflect.TypeOf(float) {
			return valueAtIndex, 's'
		}

		return valueAtIndex, 'n'

	}
	value, err := strconv.ParseFloat(term, 64)
	if err != nil {
		return term, 's'
	}
	return value, 'n'
}

func execute() {

	if len(os.Args) < 2 {
		panic("Keine Datei angegeben")
	}
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic("Datei kann nicht gelesen werden")
	}
	fileName = os.Args[1]

	lines = strings.Split(string(data), "\r\n")
	for _, line := range lines {
		terms = append(terms, strings.Split(line, " "))
	}

	var currentTerm []string
	for pointer < len(terms) {
		var isInVarNums string = "none"
		var isInVarStrings string = "none"
		var isInFuncs string = "none"
		var isInLists string = "none"
		currentTerm = terms[pointer]

		_, okF := funcs[currentTerm[0]]
		_, okN := varNums[currentTerm[0]]
		_, okS := varStrings[currentTerm[0]]
		listIndex := strings.Index(currentTerm[0], "(")
		var okL bool = false
		if listIndex != -1 {
			_, okL1 := lists[currentTerm[0][0:strings.Index(currentTerm[0], "(")]]
			if okL1 {
				okL = true
			}
		}
		switch {
		case okN:
			isInVarNums = currentTerm[0]
		case okS:
			isInVarStrings = currentTerm[0]
		case okF:
			isInFuncs = currentTerm[0]
		case okL:
			isInLists = currentTerm[0]
		}
		switch currentTerm[0] {
		case "num":
			value, valueType := checkIfVarOrList(currentTerm[3])
			if valueType != 'n' {
				panic("pexexit Wert ist keine Zahl")
			}
			varNums[currentTerm[1]] = value.(float64)
			pointer++

		case "str":
			value, valueType := checkIfVarOrList(currentTerm[3])
			if valueType != 's' {
				panic("pexexit Wert ist kein String")
			}
			varStrings[currentTerm[1]] = value.(string)
			pointer++

		case "list":
			var values []interface{}
			for _, v := range currentTerm[3:] {
				value, err := strconv.ParseFloat(v, 64)
				if err == nil {
					values = append(values, value)
				} else {
					values = append(values, v)
				}

			}
			lists[currentTerm[1]] = values
			pointer++

		case "fn":
			funcs[currentTerm[1]] = append(funcs[currentTerm[1]], pointer+1, 0)

			for terms[pointer][0] != "return" {
				pointer++
			}
			pointer++

		case "print":
			value, valueType := checkIfVarOrList(currentTerm[1])
			var text string
			switch valueType {
			case 's':
				text = value.(string)
			case 'n':
				text = fmt.Sprintf("%f", value.(float64))
			}
			fmt.Println(text)
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
				if value1 == value2 {
					for terms[pointer][0] != "}" {
						pointer++
					}
				}
				pointer++
			case "<=":
				if value1Type != 'n' || value2Type != 'n' {
					panic("<= ist nicht kompatibel mit String")
				} else {
					if value1.(float64) > value2.(float64) {
						for terms[pointer][0] != "}" {
							pointer++
						}
					}
					pointer++
				}
			case ">=":
				if value1Type != 'n' || value2Type != 'n' {
					panic(">= ist nicht kompatibel mit String")
				} else {
					if value1.(float64) < value2.(float64) {
						for terms[pointer][0] != "}" {
							pointer++
						}
					}
					pointer++
				}
			case ">":
				if value1Type != 'n' || value2Type != 'n' {
					panic("> ist nicht kompatibel mit String")
				} else {
					if value1.(float64) <= value2.(float64) {
						for terms[pointer][0] != "}" {
							pointer++
						}
					}
					pointer++
				}
			case "<":
				if value1Type != 'n' || value2Type != 'n' {
					panic("< ist nicht kompatibel mit String")
				} else {
					if value1.(float64) >= value2.(float64) {
						for terms[pointer][0] != "}" {
							pointer++
						}
					}
					pointer++
				}
			default:
				panic("Invalider Operator")

			}

		case isInVarNums:
			if len(currentTerm) > 1 {
				value, valueType := checkIfVarOrList(currentTerm[2])

				switch currentTerm[1] {
				case "=":
					if valueType != 'n' {
						panic("Num Variable kann nicht mit String belegt werden")
					} else {
						varNums[currentTerm[0]] = value.(float64)
					}
				case "+=":
					if valueType != 'n' {
						panic("Num Variable kann nicht mit String addiert werden")
					} else {
						varNums[currentTerm[0]] += value.(float64)
					}
				case "-=":
					if valueType != 'n' {
						panic("Num Variable kann nicht mit String subtrahiert werden")
					} else {
						varNums[currentTerm[0]] -= value.(float64)
					}
				case "*=":
					if valueType != 'n' {
						panic("Num Variable kann nicht mit String multipliziert werden")
					} else {
						varNums[currentTerm[0]] *= value.(float64)
					}
				case "/=":
					if valueType != 'n' {
						panic("Num Variable kann nicht mit String dividiert werden")
					} else {
						varNums[currentTerm[0]] /= value.(float64)
					}
				default:
					panic("Invalider Operator")
				}
				pointer++
			}
			pointer++

		case isInVarStrings:
			if len(currentTerm) > 1 {
				value, valueType := checkIfVarOrList(currentTerm[2])
				switch currentTerm[1] {
				case "=":
					if valueType != 's' {
						panic("String kann nicht mit Num gleichgesetzt werden")
					} else {
						varStrings[currentTerm[0]] = value.(string)
					}
				case "+=":
					if valueType != 's' {
						panic("String kann nicht mit Num gleichgesetzt werden")
					} else {
						varStrings[currentTerm[0]] += value.(string)
					}
				default:
					panic("Invalider Operator")
				}
				pointer++
			}
			pointer++

		case "while":
			value1, value1Type := checkIfVarOrList(currentTerm[1])
			value2, value2Type := checkIfVarOrList(currentTerm[3])
			if !slices.Contains(returnPositions, pointer) {
				returnPositions = append(returnPositions, pointer)
			}

			switch currentTerm[2] {
			case "==":
				if value1 != value2 {
					for terms[pointer][0] != "]" {
						pointer++
					}
					returnPositions = deleteElement(returnPositions, len(returnPositions)-1)
				}
				pointer++

			case "!=":
				if value1 == value2 {
					for terms[pointer][0] != "]" {
						pointer++
					}
					returnPositions = deleteElement(returnPositions, len(returnPositions)-1)
				}
				pointer++

			case "<=":
				if value1Type != 'n' || value2Type != 'n' {
					panic("<= ist nicht kompatibel mit String")
				} else {
					if value1.(float64) > value2.(float64) {
						for terms[pointer][0] != "]" {
							pointer++
						}
						returnPositions = deleteElement(returnPositions, len(returnPositions)-1)
					}
					pointer++

				}
			case ">=":
				if value1Type != 'n' || value2Type != 'n' {
					panic(">= ist nicht kompatibel mit String")
				} else {
					if value1.(float64) < value2.(float64) {
						for terms[pointer][0] != "]" {
							pointer++
						}
						returnPositions = deleteElement(returnPositions, len(returnPositions)-1)
					}
					pointer++

				}
			case ">":
				if value1Type != 'n' || value2Type != 'n' {
					panic("> ist nicht kompatibel mit String")
				} else {
					if value1.(float64) <= value2.(float64) {
						for terms[pointer][0] != "]" {
							pointer++
						}
						returnPositions = deleteElement(returnPositions, len(returnPositions)-1)
					}
					pointer++

				}
			case "<":
				if value1Type != 'n' || value2Type != 'n' {
					panic("< ist nicht kompatibel mit String")
				} else {
					if value1.(float64) >= value2.(float64) {
						for terms[pointer][0] != "]" {
							pointer++
						}
						returnPositions = deleteElement(returnPositions, len(returnPositions)-1)
					}
					pointer++

				}
			default:
				panic("Invalider Operator")
			}
		case "]":
			pointer = returnPositions[len(returnPositions)-1]

		case isInFuncs:
			funcs[currentTerm[0]][1] = pointer + 1
			pointer = funcs[currentTerm[0]][0]

		case "return":
			pointer = funcs[currentTerm[1]][1]

		case "ereturn":
			pointer = funcs[currentTerm[1]][1]

		case "input":

			_, okN := varNums[currentTerm[1]]
			_, okS := varStrings[currentTerm[1]]
			if okN {
				var input string
				fmt.Scanf("%s\n", &input)
				value, err := strconv.ParseFloat(input, 64)
				if err != nil {
					panic("Inkompatibler Datentyp")
				}
				varNums[currentTerm[1]] = value
			} else if okS {
				var input string
				fmt.Scanf("%s\n", &input)
				value := input
				varStrings[currentTerm[1]] = value
			} else {
				panic("Variable nicht vorhanden")
			}
			pointer++

		case isInLists:
			var index string
			index = currentTerm[0][strings.Index(currentTerm[0], "(")+1 : strings.Index(currentTerm[0], ")")]
			value, valueType := checkIfVarOrList(index)
			value2, _ := checkIfVarOrList(currentTerm[2])
			if valueType != 'n' {
				panic("Index ist keine Zahl")
			} else {
				indexInt := int64(value.(float64))
				lists[currentTerm[0][0:strings.Index(currentTerm[0], "(")]][indexInt] = value2
				pointer++
			}
		case "append":
			value, _ := checkIfVarOrList(currentTerm[2])
			lists[currentTerm[1]] = append(lists[currentTerm[1]], value)
			pointer++

		case "clear":
			fmt.Printf("\x1bc")
			pointer++

		case "random":
			value1, valueType := checkIfVarOrList(currentTerm[2])
			value2, value2Type := checkIfVarOrList(currentTerm[3])
			if valueType != 'n' || value2Type != 'n' {
				panic("Keine Zahl bei random angegeben")
			} else {
				valueRange := value2.(float64) - value1.(float64)
				newValue := rand.Int64N(int64(valueRange)) + int64(value1.(float64))
				varNums[currentTerm[1]] = float64(newValue)
				pointer++
			}
		default:
			pointer++
		}

	}
	panic("Programm beendet")
}

func main() {
	varNums = make(map[string]float64)
	varStrings = make(map[string]string)
	lists = make(map[string][]interface{})
	funcs = make(map[string][]int)

	execute()
}
