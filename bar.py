#!/usr/bin/python
import os
from termcolor import colored
import builtins
import sys

def drawGraph(label:str, unit:str, val:float, start:float, end:float, color="white", precision=3, numTicks=10, length=-1):
       
        if(start == end):
            return "BAR range 0 not supported"
        # Translate min to 0 to make everything easier
        # Only the displayed data will be translated back

        filtered_val = float(min(end, max(start, val)))
        
        tick = '┼'
        hLine = '─'
        vLine = '│'
        c0 = '├'
        c1 = '┤'
        c2 = '└'
        c3 = '┘'
        c4 = '┌'
        c5 = '┐'
        blocks = ["","▏","▎","▍","▌","▋","▊","▉","█"]
        blockSpace = ' '
        space = ' '
        
        output = ""
        
        # Figure out how many columns to use
        columns = 100 
        if(length < 0):
            size = os.get_terminal_size()
            terminal_columns = size.columns  
            length = max(-1,length)
            columns = int((length * -1) * terminal_columns)
            last_tick_label = f"{round(float(end),precision):g}{unit}".replace(" ", "")
            columns = min(columns, terminal_columns - (len(last_tick_label)))
        else:
            columns = int(length)
       

        # columns must be evenly divisible by numTicks
        columns -= columns % numTicks



        # Generate the title line
        output += f"{label} {round((val), precision):g}{unit} \n"

        # Generate tick labels
        tick_labels = []
        tick_val = start
        for i in range(numTicks + 1):
            tick_labels.append(tick_val)                
            tick_val += (end - start) / (numTicks)


        # Generate the tick labels in the correct position 
        tick_spacing = int((columns - numTicks) / numTicks)
        for i in range(numTicks):
            formatted_label = f"{round(float(tick_labels[i]),precision):g}{unit}".replace(" ", "")
            output += formatted_label + (" " * (tick_spacing - len(formatted_label) + 1)) 
        
        output+=(f"{round(float(end),precision):g}{unit}".replace(" ", ""))
        output += "\n"
        
        # Generate the tick line
        tick_line = c4
        for i in range(numTicks-1):
            tick_line += (hLine * tick_spacing) + tick
        tick_line += hLine * tick_spacing
        tick_line += c5
        tick_line += "\n"
        output += tick_line
        
        # Calculate a dictionary that maps values to number of chars
        tick_locations = {start:0}
        current_length = 0
        for i in range(1,numTicks):
            tick_index = tick_line.index(tick)
            tick_locations[tick_labels[i]] =  (tick_index - .5) + current_length
            current_length += tick_index + 1
            tick_line = tick_line[tick_index+1:]
        tick_locations[end] = columns - 1


        
        output += vLine 
        
        
        # Generate the data BAR
        
        # Find what sector the value is in 
        sector = 0
        for i in range(len(tick_labels) - 1):
            if(val > tick_labels[i] and val <= tick_labels[i+1]):
                sector = i
    
        bar_length = 0

        # Get the number of characters to fill the previous sectors
        bar_length += tick_locations[tick_labels[sector]]

        # Get the number of characters to fill the current sector
        percent_in_sector = (val - tick_labels[sector]) / (tick_labels[sector + 1] - tick_labels[sector]) 
        characters_in_sector = tick_locations[tick_labels[sector + 1]] - tick_locations[tick_labels[sector]]
        bar_length += percent_in_sector * characters_in_sector
        
        # Fill bar_chars with bar_length characters
        bar_chars = ""
        remainder = bar_length - int(bar_length)
        bar_chars += blocks[8] * int(bar_length)
        block_index = int(remainder * (len(blocks)))
        bar_chars += blocks[block_index]        
        
        # Fill in the rest of the data BAR with spaces and the end char
        output += colored(bar_chars, color)
        output += ((columns - len(bar_chars)) - 1) * blockSpace
        output += vLine
        

        # Generate the bottom of the bar
        output += "\n"
        output += c2
        output += hLine * (columns - 1)
        output += c3

        return output    


def help():
    print("--BAR--")

if __name__ == "__main__":

    label = ""
    unit = ""
    val = ""
    start = ""
    end = ""
    color = "white"
    length = -.8 
    precision = 3
    numTicks = 5
    try:
        label = sys.argv[1]
        unit = sys.argv[2]
        val = float(sys.argv[3])
        start = float(sys.argv[4])
        end = float(sys.argv[5])
    except:
        print("-Argument Error-\nUsage: bar <label> <unit> <val> <start> <end> [args]")
        exit() 

    for i in range(len(sys.argv)):
        if(sys.argv[i] == "help" or sys.argv[i] == "-h" or sys.argv[i] == "--help"):
            help()
            exit()
        try:
            if(sys.argv[i] == "--color"):
                color = sys.argv[i+1]
            if(sys.argv[i] == "--length"):            
                length = float(sys.argv[i+1])
            if(sys.argv[i] == "--precision"):
                precision = int(sys.argv[i+1])
            if(sys.argv[i] == "--ticks"):
                numTicks = int(sys.argv[i+1])
        except:
            pass

    print(drawGraph(label, unit, val, start, end, color=color, length=length,precision=precision,numTicks=numTicks))
