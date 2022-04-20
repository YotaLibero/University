using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Antlr.Runtime;

namespace TranslatorLab
{
    public class Emitter
    {
        private int countCycle = 0;
        private int countIf = 0;
        private int countSwitch = 0;
        private string variableSwitch = "s7";

        public Emitter()
        {

        }

        private Dictionary<string, VariableInfo> variableTable = new Dictionary<string, VariableInfo>();
        private StringBuilder methodBody = new StringBuilder();

        private class VariableInfo
        {
            public VariableInfo(string name)
            {
                Name = name;
            }
            public string Name {
                get;
                set;
            }
        }

        public void AddIfLabel(bool first = false)
        {
            if (first)
            {
                countIf++;
                methodBody.AppendLine("GOFALSE ELSE" + countIf.ToString());
            }
            else
            {
                methodBody.AppendLine("ELSE" + countIf.ToString()+":");
            }
        }

        public void AddSwitchLabel(bool first = false, bool next = false, string constant = "")
        {
            if (first)
            {
                countSwitch++;
                variableSwitch = variableSwitch + countSwitch.ToString() + "w";
                AddLValue(variableSwitch);
            } else
            {
                if(next)
                {
                    AddLoadID(variableSwitch);
                    AddLoadConst(constant);
                    AddOperation("==");
                    methodBody.AppendLine("GOFALSE NEXT" + countSwitch.ToString() + constant.ToString().Trim('\''));
                }
                else
                {
                    methodBody.AppendLine("NEXT" + countSwitch.ToString() + constant.ToString().Trim('\'') + ":");
                }
            }
        }

        public void AddCycleLabel(bool first = false, bool conditionExist = false,
            bool conditionNotExist = false, bool iter = false, bool prog = false)
        {
            if(first)
            {
                countCycle++;
                methodBody.AppendLine("CYCLE" + countCycle.ToString() + ":");
            }
            else if (conditionExist)
            {
                methodBody.AppendLine("GOFALSE ENDCYCLE" + countCycle.ToString());
            }
            else if(conditionNotExist)
            {
                methodBody.AppendLine("GOTO PROGCYCLE" + countCycle.ToString());
                methodBody.AppendLine("ITERCYCLE" + countCycle.ToString() + ":");
            }
            else if(iter)
            {
                methodBody.AppendLine("GOTO CYCLE" + countCycle.ToString());
                methodBody.AppendLine("PROGCYCLE" + countCycle.ToString()+":");
            }
            else if(prog)
            {
                methodBody.AppendLine("GOTO ITERCYCLE" + countCycle.ToString());
                methodBody.AppendLine("ENDCYCLE" + countCycle.ToString()+":");
            }
        }

        public void AddDeclarationStatement(string variableName, string constant = "", bool assignment = false)
        {
            if (!variableTable.Keys.Contains(variableName)) {
                variableTable.Add(variableName, new VariableInfo(variableName));
            }
            if (assignment) {
                AddLValue(variableName);
                AddLoadConst(constant);
                AddAssignStatement();
            }
        }

        public void AddDecOrInc(string variableName, string op)
        {
            AddLValue(variableName);
            AddLoadConst("1");
            AddOperation(op);
            AddAssignStatement();
        }

        void WriteLocals(StreamWriter outWriter)
        {
            if (variableTable.Count == 0) return;
            StringBuilder localsString = new StringBuilder();
            foreach (VariableInfo variable in variableTable.Values)
            {
                localsString.Append(variable.Name + " DW\n");
            }
            localsString.Remove(localsString.Length - 1, 1);
            localsString.Append(" \n");
            outWriter.WriteLine(localsString.ToString());
        }

        void WriteMethodBody(StreamWriter outWriter)
        {
            methodBody.AppendLine("HALT");
            outWriter.WriteLine(methodBody.ToString());
        }

        public void SaveMSIL(string fileName)
        {
            StreamWriter outWriter = new StreamWriter(File.Create(fileName), new System.Text.UTF8Encoding(true));
            WriteLocals(outWriter);
            WriteMethodBody(outWriter);
            outWriter.Flush();
        }

        public void AddAssignStatement()
        {
            methodBody.AppendLine(":=");
        }

        public void AddLValue(string variableName)
        {
            if (!variableTable.Keys.Contains(variableName))
            {
                variableTable.Add(variableName, new VariableInfo(variableName));
            }
            methodBody.AppendLine("LVALUE " + variableName);
        }

        public void AddLoadID(string variableName)
        {
            if (!variableTable.Keys.Contains(variableName))
            {
                variableTable.Add(variableName, new VariableInfo(variableName));
            }
            methodBody.AppendLine("RVALUE " + variableName);
        }

        public void AddLoadConst(string constant)
        {
            methodBody.AppendLine("PUSH " + constant);
        }

        public void AddOperation(string op)
        {
            switch (op)
            {
                case "+": methodBody.AppendLine("ADD"); break;
                case "-": methodBody.AppendLine("SUB"); break;
                case "*": methodBody.AppendLine("MULT"); break;
                case "/": methodBody.AppendLine("DIV"); break;
                case "++": methodBody.AppendLine("ADD"); break;
                case "--": methodBody.AppendLine("SUB"); break;
                case "&&": methodBody.AppendLine("MULT"); break;
                case "||": methodBody.AppendLine("ADD"); break;
                case ">": methodBody.AppendLine(">"); break;
                case ">=": methodBody.AppendLine(">="); break;
                case "<": methodBody.AppendLine("<"); break;
                case "<=": methodBody.AppendLine("<="); break;
                case "==": methodBody.AppendLine("=="); break;
                case "!=": methodBody.AppendLine("!="); break;
                default: break;
            }
        }
    }
    class Program
    {
        static void Main(string[] args)
        {
            StringWriter logBufferParser = new StringWriter();
            StringWriter logBufferLexer = new StringWriter();
            Emitter emitter = new Emitter();
            ANTLRFileStream inStream = new ANTLRFileStream("input.txt");
            courseworkLexer lexer = new courseworkLexer(inStream);
            lexer.TraceDestination = logBufferLexer;
            CommonTokenStream tokenStream = new CommonTokenStream(lexer);
            courseworkParser parser = new courseworkParser(tokenStream, emitter);
            parser.TraceDestination = logBufferParser;
            try
            {
                parser.start_rule();
                emitter.SaveMSIL("result.txt");
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
            if (parser.NumberOfSyntaxErrors != 0 || lexer.NumberOfSyntaxErrors != 0)
            {
                Console.WriteLine(logBufferLexer.ToString());
                Console.WriteLine(logBufferParser.ToString());
            }
            else Console.WriteLine("Трансляция завершена успешно");
            Console.ReadKey();
        }
    }
}
