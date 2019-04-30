//import processing.dxf.*;
//import processing.svg.*;

// Borrowed from https://github.com/zmorph/codeplastic/blob/master/circle_packing/circle_packing.pde
// To run with Processing

Pack pack;

boolean growing = false;
int n_start = 10;

void setup() {
  size(384, 216);

  noFill();
  strokeWeight(1.5);
  stroke(5);

  noiseDetail(2, 0.1);

  pack = new Pack(n_start);
}

void draw() {
  background(#f5f4f4);

  pack.run();

  if (growing)
    pack.addCircle(new Circle(width/2, height/2));

  //saveFrame("frames/#####.tif");
}

public class PVector {
  public float x;
  public float y;
  public float z;
  
  public PVector() {}
  
  public PVector(float x, float y) {
    this.x = x;
    this.y = y;
  }
  public PVector(float x, float y, float z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }

  public float mag() {
    return (float) Math.sqrt(x*x + y*y + z*z);
  }
  
  public PVector add(PVector v) {
    x += v.x;
    y += v.y;
    z += v.z;
    return this;
  }

  public PVector add(float x, float y) {
    this.x += x;
    this.y += y;
    return this;
  }

  public PVector sub(PVector v) {
    x -= v.x;
    y -= v.y;
    z -= v.z;
    return this;
  }
  
  public PVector div(float n) {
    x /= n;
    y /= n;
    z /= n;
    return this;
  } 
  
  public PVector setMag(float len) {
    normalize();
    mult(len);
    return this;
  }
  public PVector normalize() {
    float m = mag();
    if (m != 0 && m != 1) {
      div(m);
    }
    return this;
  }  
  public PVector mult(float n) {
    x *= n;
    y *= n;
    z *= n;
    return this;
  }
  public PVector limit(float max) {
    if (magSq() > max*max) {
      normalize();
      mult(max);
    }
    return this;
  }
  
  public float magSq() {
    return (x*x + y*y + z*z);
  }
  public PVector set(float x, float y, float z) {
    this.x = x;
    this.y = y;
    this.z = z;
    return this;
  }
}

  static public float dist(PVector v1, PVector v2) {
    float dx = v1.x - v2.x;
    float dy = v1.y - v2.y;
    float dz = v1.z - v2.z;
    return (float) Math.sqrt(dx*dx + dy*dy + dz*dz);
  }
  
  static public PVector sub(PVector v1, PVector v2) {
    return sub(v1, v2, null);
  }

  static public PVector sub(PVector v1, PVector v2, PVector target) {
    PVector ret = null;
    if (target == null) {
      ret = new PVector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z);
    } else {
      target.set(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z);
      ret = target;
    }
    return target;
  }
  
//--------------------------------------------------------------------------------


class Pack {
  ArrayList<Circle> circles;

  float max_speed = 1;
  float max_force = 1;

  float border = 5;

  float min_radius = 10;
  float max_radius = 200;

  Pack(int n) {  
    initiate(n);
  }

  void initiate(int n) {
    circles = new ArrayList<Circle>(); 
    for (int i = 0; i < n; i++) {
      addCircle(new Circle(width/2, height/2));
    }
  }

  void addCircle(Circle b) {
    circles.add(b);
  }

  void run() {

    PVector[] separate_forces = new PVector[circles.size()];
    int[] near_circles = new int[circles.size()];

    for (int i=0; i<circles.size(); i++) {
      checkBorders(i);
      updateCircleRadius(i);
      applySeparationForcesToCircle(i, separate_forces, near_circles);
      displayCircle(i);
    }
  }

  void checkBorders(int i) {
    Circle circle_i=circles.get(i);
    if (circle_i.position.x-circle_i.radius/2 < border)
      circle_i.position.x = circle_i.radius/2 + border;
    else if (circle_i.position.x+circle_i.radius/2 > width - border)
      circle_i.position.x = width - circle_i.radius/2 - border;
    if (circle_i.position.y-circle_i.radius/2 < border)
      circle_i.position.y = circle_i.radius/2 + border;
    else if (circle_i.position.y+circle_i.radius/2 > height - border)
      circle_i.position.y = height - circle_i.radius/2 - border;
  }

  void updateCircleRadius(int i) {
    circles.get(i).updateRadius(min_radius, max_radius);
  }

  void applySeparationForcesToCircle(int i, PVector[] separate_forces, int[] near_circles) {

    if (separate_forces[i]==null)
      separate_forces[i]=new PVector();

    Circle circle_i=circles.get(i);

    for (int j=i+1; j<circles.size(); j++) {

      if (separate_forces[j] == null) 
        separate_forces[j]=new PVector();

      Circle circle_j=circles.get(j);

      PVector forceij = getSeparationForce(circle_i, circle_j);

      if (forceij.mag()>0) {
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
  }

  PVector getSeparationForce(Circle n1, Circle n2) {
    PVector steer = new PVector(0, 0, 0);
    float d = dist(n1.position, n2.position);
    if ((d > 0) && (d < n1.radius/2+n2.radius/2 + border)) {
      PVector diff = PVector.sub(n1.position, n2.position);
      diff.normalize();
      diff.div(d);
      steer.add(diff);
    }
    return steer;
  }

  String getSaveName() {
    return  day()+""+hour()+""+minute()+""+second();
  }

  void exportSVG() {
    String exportName = getSaveName()+".svg";
    PGraphics pg = createGraphics(width, height, SVG, exportName);
    pg.beginDraw();
    pg.rect(0, 0, width, height);
    for (int i=0; i<circles.size(); i++) {
      Circle p = circles.get(i);
      pg.ellipse(p.position.x, p.position.y, p.radius, p.radius);
    } 
    pg.endDraw();
    pg.dispose();
    println(exportName + " saved.");
  }

  void displayCircle(int i) {
    circles.get(i).display();
  }
}

class Circle {

  PVector position;
  PVector velocity;
  PVector acceleration;

  float radius = 1;

  Circle(float x, float y) {
    acceleration = new PVector(0, 0);
    velocity = PVector.random2D();
    position = new PVector(x, y);
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

  void updateRadius(float min, float max) {
    radius = min + noise(position.x*0.01, position.y*0.01) * (max-min);
  }

  void display() {
    ellipse(position.x, position.y, radius, radius);
  }
}

void mouseDragged() {
  pack.addCircle(new Circle(mouseX, mouseY));
}

void mouseClicked() {
  pack.addCircle(new Circle(mouseX, mouseY));
}
