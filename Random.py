def randomMove(board,tile):
  newBoard = getBoardCopy(board)
  move = random.choice(getValidMoves(newBoard,tile))# สุ่มที่วางจากที่ที่วางใด้ทั้งหมด
  return move
