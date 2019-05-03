// Inspired by https://github.com/zmorph/codeplastic/blob/master/circle_packing/circle_packing.pde
// To run in Processing IDE

float border = 0;

int canvasWidth = 1778;
int canvasHeight = 1000;

float minRadius = 50;
float maxRadius = 700;

// stop process controls
int maxIterations = 1000;
int checkIteration = 50;
float minShiftAtCheck = 25;

//Pack pack;
Table table;  
SequencePacker sequencePacker = new SequencePacker(table);

void setup() {
  table = loadTable("../packing_input.csv", "header");
  println(table.getRowCount() + " total rows in table"); 
  
  size(1778, 1000); //no variables allowed!
  noFill();
  strokeWeight(1.5);
  stroke(5);
  smooth();
  randomSeed(11);
  //noiseDetail(2, 0.1);

}

// Main entry
void draw() {
  background(#f5f4f4);
  sequencePacker.run();
}


// processing class
class SequencePacker {
  Table data;
  Pack curPack;
  int frameNum;
  ArrayList<ArrayList<Circle>> frameCirclesArr;

  SequencePacker(Table data) {
    this.data = data;
  }  
  
  void init() {
    frameNum = -1;
    //Calculate real min/max radii
    float minCurRad = 0;
    float maxCurRad = 0;
    for (TableRow row : table.rows()) {
      int count = row.getInt("count");
      if (minCurRad > 0 && minCurRad > count) {
        minCurRad = count;
      }
      if (maxCurRad < count) {
        maxCurRad = count;
      }
    }
    println("...Counts: min=" + minCurRad + ", max=" + maxCurRad);
    
    // scale
    float radScale = (maxRadius - minRadius)/(maxCurRad - minCurRad);
    
    // get circles for each frame
    frameCirclesArr = new ArrayList<ArrayList<Circle>>();
    ArrayList<Circle> circles = null; 
    int curDay = -1;
    int i = 0;
    for (TableRow row : table.rows()) {
      //String date = row.getString("date");
      //int cluster = row.getInt("cluster");
      int count = row.getInt("count");
      int day = row.getInt("day");
      
      // new day
      if (day != curDay) {
        println("....Day: " + day);
        i = 0;
        curDay = day;
        circles = new ArrayList<Circle>();
        frameCirclesArr.add(circles);
      }
      
      float radius = minRadius + radScale * count;
      if (count <= 0) {
        radius = minRadius/100;
      }
      
      PVector offset = getSpiralOffset(i, width/2, height/2, height/5, 50, -5, 0);
      circles.add(new Circle(offset.x, offset.y, radius));
      i++;
    }  
    
    curPack = new Pack();
    if(!nextFrame()) {
      println("...stopped");
      stop();
    }
  }
  
  // Get coordinate of the point on a spiral
  // i - point number
  // centerX-- X origin of the spiral.
  // centerY-- Y origin of the spiral.
  // radius--- Distance from origin to outer arm.
  // sides---- Number of points or sides along the spiral's arm.
  // coils---- Number of coils or full rotations. (Positive numbers spin clockwise, negative numbers spin counter-clockwise)
  // rotation- Overall rotation of the spiral. ('0'=no rotation, '1'=360 degrees, '180/360'=180 degrees)
  PVector getSpiralOffset(int i, float centerX, float centerY, float radius, float sides, float coils, float rotation) {
    float awayStep = radius/sides;              // How far to step away from center for each side.
    float aroundStep = coils/sides;             // How far to rotate around center for each side.
    float aroundRadians = aroundStep * TWO_PI;  //Convert aroundStep to radians.
    rotation *= TWO_PI;                         // Convert rotation to radians.
    float away = i * awayStep;                  // How far away from center
    float around = i * aroundRadians + rotation;// How far around the center.
    
    return new PVector(centerX + cos(around) * away, centerY + sin(around) * away);
  } 
  
  ArrayList<Circle> getNextCirclesSet() {
    int len = frameCirclesArr.size();
    if (frameNum >= len) {
      return null;
    }
    return frameCirclesArr.get(frameNum);
  }
  
  // Frame management
  boolean nextFrame() {
    boolean ret = false;
    
    if (frameNum >= 0) {
      println("...  finished frame: " + frameNum);
     //TODO 
    }

    // next frames
    frameNum++;
    ArrayList<Circle> circles = getNextCirclesSet();
    if (circles != null) {
      curPack.setStrategy(new SimpleBoxStrategy());
      
      ArrayList<Circle> curCircles = curPack.circles; 
      if (curCircles == null) {
        //set first day circles
        curPack.setCircles(circles);
      } else {
        // just update the radii
        for (int i=0; i < curCircles.size(); i++) {
          curCircles.get(i).radius = circles.get(i).radius;
        }
      }
      
      ret = true;
    }
    return ret;
  }
  
  void run() {
    if (curPack == null) {
      init();
    }

    int ret = curPack.run();
    if (ret != 0) {
      if(!nextFrame()) {
        println("...stopped");
        stop();
      }
    }
  }
} // end class SequencePacker

interface RunStrategy {
  int run(Pack pack);
}

public class SimpleBoxStrategy implements RunStrategy {
  long iteration = 0;
  float w = canvasWidth;
  float h = canvasHeight;
  float maxPosChange = 0;
  ArrayList<PVector> checkArr = new ArrayList<PVector>(50);

  // draws the current iteration of the scene.
  // re-entarable 
  public int run(Pack pack) 
  {
    pack.setBoxHeight(h);
    pack.setBoxWidth(w);
    
    boolean checkPoint = iteration%checkIteration == 0 && iteration > 0;
    
    // draw box    
    noFill();
    stroke(200);
    rect((canvasWidth-w)/2, (canvasHeight-h)/2,w,h);
    
    PVector[] separate_forces = new PVector[pack.circles.size()];
    int[] near_circles = new int[pack.circles.size()];
    
    if (++iteration >= maxIterations) {
      println("stopped: max iterations reached: " +  maxIterations);
      return -1;
    }
    
    // get positions and draw all circles
    PVector centerGravity = new PVector(canvasWidth/2, canvasHeight/2, 0);
    boolean forced = false;
    for (int i=0; i < pack.circles.size(); i++) {
      Circle cs = pack.circles.get(i);
      pack.checkBorders(i);
      if (pack.applySeparationForcesToCircle(i, separate_forces, near_circles, centerGravity)) {
        forced = true;
      }
      pack.displayCircle(i);

      // check for stop due to stability
      if (iteration == 1) {
        checkArr.add(new PVector(cs.position.x, cs.position.y));
      }
      if (checkPoint) {
        float mag = checkArr.get(i).dist(new PVector(cs.position.x, cs.position.y));
        //skipping fake circles
        if (cs.radius >= minRadius && maxPosChange < mag) {
          maxPosChange = mag;
        }
        checkArr.set(i, new PVector(cs.position.x, cs.position.y));
      }
    }
    
    if (checkPoint) {
      println ("iteration " + (iteration-1) + ", maxPosChange=" + maxPosChange);
      if (maxPosChange < minShiftAtCheck) {
        println("stopped: stability after " + iteration + " iterations");
        return 2; //finished successfully
      }
      maxPosChange = 0;
    }
    
    
    // would stop only when no gravity applied
    if (!forced) {
      println("success after " + iteration + " iterations");
      return 1; //finished successfully
    }
    
    return 0; //not finished
  }
  
}


/**
  Pack class
**/
public class Pack {
  private ArrayList<Circle> circles;
  private RunStrategy strategy;
  private float max_speed = 1;
  private float max_force = 1;
  
  // borders
  private float left;
  private float right;
  private float up;
  private float down;

  public int run() {
    return strategy.run(this);
  }

  public void setStrategy(RunStrategy strategy) {
    this.strategy = strategy;
  }

  public void setCircles(ArrayList<Circle> circles) {
    this.circles = circles;
  }
  
  public void setBoxWidth(float val) {
    if (val <= 0) val = canvasWidth;
    left = (width - val)/2 + border;
    right = left + val - 2*border;
  }
  
  public void setBoxHeight(float val) {
    if (val <= 0) val = canvasHeight;
    down = (height - val)/2 + border;
    up = down + val - 2*border;
  }
  
  private void checkBorders(int i) {
    
    Circle circle_i=circles.get(i);
    
    if (circle_i.position.x-circle_i.radius/2 < left)
      circle_i.position.x = circle_i.radius/2 + left;
    else if (circle_i.position.x+circle_i.radius/2 > right)
      circle_i.position.x = right - circle_i.radius/2;
    if (circle_i.position.y-circle_i.radius/2 < down)
      circle_i.position.y = circle_i.radius/2 + down;
    else if (circle_i.position.y+circle_i.radius/2 > up)
      circle_i.position.y = up - circle_i.radius/2;
  }

  private boolean applySeparationForcesToCircle(
    int i, PVector[] separate_forces, int[] near_circles,
    PVector centerGravity)
  {
    boolean forced = false;
    
    if (separate_forces[i] == null)
      separate_forces[i]=new PVector();

    Circle circle_i=circles.get(i);

    // add separation forces from all surrounding circles
    for (int j=i+1; j<circles.size(); j++) {

      if (separate_forces[j] == null) 
        separate_forces[j]=new PVector();

      Circle circle_j=circles.get(j);

      PVector forceij = getSeparationForce(circle_i, circle_j);

      if (forceij.mag()>0) {
        forced = true;
        separate_forces[i].add(forceij);        
        separate_forces[j].sub(forceij);
        near_circles[i]++;
        near_circles[j]++;
      }
    }

    if (near_circles[i] > 0) {
      separate_forces[i].div((float)near_circles[i]);
    }
    
    if (separate_forces[i].mag() > 0) {
      forced = true;
      separate_forces[i].setMag(max_speed);
      separate_forces[i].sub(circles.get(i).velocity);
      separate_forces[i].limit(max_force);
    } 
    else if (true && centerGravity != null) {
      // add center gravity force if not forced out
      forced = true;
      PVector vgf = getGravityForce(circle_i, centerGravity);
      separate_forces[i].sub(vgf);
    }

    PVector separation = separate_forces[i];

    circles.get(i).applyForce(separation);
    circles.get(i).update();

    // If they have no intersecting neighbours they will stop moving.
    // Only effective when no gravity
    if (centerGravity == null) {
      circle_i.velocity.x = 0.0;
      circle_i.velocity.y = 0.0;
    }
    
    return forced;
  }

  private PVector getSeparationForce(Circle n1, Circle n2) {
    PVector steer = new PVector(0, 0, 0);
    float d = PVector.dist(n1.position, n2.position);
    if ((d > 0) && (d < n1.radius/2+n2.radius/2 + border)) {
      PVector diff = PVector.sub(n1.position, n2.position);
      diff.normalize();
      diff.div(d);
      steer.add(diff);
    }
    return steer;
  }

  private PVector getGravityForce(Circle n1, PVector centerGravity) {
    PVector steer = new PVector(0, 0, 0);
    PVector diff = PVector.sub(n1.position, centerGravity);
    diff.normalize();
    float c = n1.radius/350;
    diff.mult(c*c); //proportional to radius
    steer.add(diff);
    return steer;
  }

  void displayCircle(int i) {
    circles.get(i).display();
  }
  
}


/*
  Circle class
*/
class Circle {

  PVector position;
  PVector velocity;
  PVector acceleration;
  float radius;

  Circle(float x, float y, float radius) {
    acceleration = new PVector(0, 0);
    velocity = PVector.random2D();
    position = new PVector(x, y);
    this.radius = radius;
  }

  void applyForce(PVector force) {
    acceleration.add(force);
  }

  void update() {
    //velocity.add(noise(100+position.x*0.01, 100+position.y*0.01)*0.5, noise(200+position.x*0.01, 200+position.y*0.01)*0.5); 
    velocity.add(acceleration);
    position.add(velocity);
    acceleration.mult(0);
  }

  void display() {
    //fill(255, 200, 200);
    fill(255);
    stroke(100);
    ellipse(position.x, position.y, radius, radius);
  }
}
