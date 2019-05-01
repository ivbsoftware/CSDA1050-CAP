// Inspired by https://github.com/zmorph/codeplastic/blob/master/circle_packing/circle_packing.pde
// To run in Processing IDE

int n_circles = 36;
float border = 0;
float min_radius = 20;
float max_radius = 100;

int canvasWidth = 1000;
int canvasHeight = 600;

Pack pack;

// Main
void draw() {
  background(#f5f4f4);
  pack.run();
}

void setup() {
  size(1000, 600); //no variables allowed!
  noFill();
  strokeWeight(1.5);
  stroke(5);
  noiseDetail(2, 0.1);

  ArrayList<Circle> circles = initiateCircles(n_circles);
  pack = new Pack(circles, new SimpleBoxStrategy());
}

ArrayList<Circle> initiateCircles (int n) {
  ArrayList<Circle> circles = new ArrayList<Circle>(); 
  for (int i = 0; i < n; i++) {
    float radius = min_radius + (max_radius - min_radius)/n * (n-i);
    float delta = (i%2==0?-1.:1.) * i * 15; 
    circles.add(new Circle(width/2 + delta, height/2, radius));
  }
  
  return circles;
}

interface RunStrategy {
  void run(Pack pack);
}

public class SimpleBoxStrategy implements RunStrategy {
  long iteration = 0;
  
  void run(Pack pack) {
    
    float w = 600;
    float h = 280;
    
    
    pack.setBoxHeight(h);
    pack.setBoxWidth(w);
    
    // draw box    
    noFill();
    stroke(200);
    rect((canvasWidth-w)/2, (canvasHeight-h)/2,w,h);
    
    PVector[] separate_forces = new PVector[pack.circles.size()];
    int[] near_circles = new int[pack.circles.size()];
    
    if (++iteration >= 1000) {
      println("stopped after 1000 iterations");
      stop();
    }
    
    //println("iteration " + iteration);
    
    boolean forced = false;
    for (int i=0; i < pack.circles.size(); i++) {
      pack.checkBorders(i);
      if (pack.applySeparationForcesToCircle(i, separate_forces, near_circles)) {
        forced = true;
      }
      pack.displayCircle(i);
    }
    
    if (!forced) {
      println("stopped...");
      stop();
    }
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
  private float border;
  
  // borders
  private float left;
  private float right;
  private float up;
  private float down;

  public Pack(ArrayList<Circle> circles, RunStrategy strategy) {
    this.strategy = strategy;
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
  
  private void run() {
    strategy.run(this);
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
    int i, PVector[] separate_forces, int[] near_circles)
  {
    boolean forced = false;
    
    if (separate_forces[i]==null)
      separate_forces[i]=new PVector();

    Circle circle_i=circles.get(i);

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

    if (near_circles[i]>0) {
      separate_forces[i].div((float)near_circles[i]);
    }

    if (separate_forces[i].mag() >0) {
      forced = true;
      separate_forces[i].setMag(max_speed);
      separate_forces[i].sub(circles.get(i).velocity);
      separate_forces[i].limit(max_force);
    }

    PVector separation = separate_forces[i];

    circles.get(i).applyForce(separation);
    circles.get(i).update();

    // If they have no intersecting neighbours they will stop moving
    circle_i.velocity.x = 0.0;
    circle_i.velocity.y = 0.0;
    
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

  private void displayCircle(int i) {
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
