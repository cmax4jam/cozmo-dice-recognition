class Yahtzee(StateMachineProgram):
    def __init__(self):
        super().__init__(cam_viewer=False)
        self.foundDice = []
        self.dicePose = []

    def user_image(self,image,gray):
        self.robot.myimage = gray

    class FindDice(StateNode):
        def start(self,event):
            super().start(event)
            image = self.robot.myimage 
            blurred = cv2.GaussianBlur(image, (5, 5), 0)
            _, image_thresh = cv2.threshold(blurred, 105, 255, 0, cv2.THRESH_BINARY)
            contours,_ = cv2.findContours(image_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            areas = [(i, cv2.contourArea(contours[i])) for i in range(len(contours))]
            areas.sort(key=lambda x: x[1])
            areas.reverse()
            minArea = 100
            maxArea = 1000
            for area_entry in areas:
                if area_entry[1] < minArea or area_entry[1] > maxArea:
                    continue
                index = area_entry[0]
                contour = contours[index]
                self.parent.foundDice.append(contour)

            for diceContours in self.parent.foundDice:
                M = cv2.moments(diceContours)
       	        cX = int(M['m10'] / M['m00'])
	            cY = int(M['m01'] / M['m00'])         

                