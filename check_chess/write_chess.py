"""Write chess in json file."""

import json
with open('chess.json','w') as file:
    chess = """
{
"board":[
    ["brook","bknight","bbishop","bqueen","bking","bbishop","bknight","brook"],
    ["bpawn","bpawn","bpawn","bpawn","bpawn","bpawn","bpawn","bpawn"],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    ["wpawn","wpawn","wpawn","wpawn","wpawn","wpawn","wpawn","wpawn"],
    ["wrook","wknight","wbishop","wqueen","wking","wbishop","wknight","wrook"]
],
"figures":{
	"wking": "♔ ",
	"wqueen": "♕ ",
	"wbishop": "♗ ",
	"wknight": "♘ ",
	"wrook": "♖ ",
	"wpawn": "♙ ",
	"bking": "♚ ",
	"bqueen": "♛ ",
	"bbishop": "♝ ",
	"bknight": "♞ ",
	"brook": "♜ ",
	"bpawn": "♟ "
    }
}
    """
    data = json.loads(chess)
    json.dump(data, file, indent=4)
