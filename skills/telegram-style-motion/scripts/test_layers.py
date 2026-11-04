import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageChops
from layers import LayerPlan

class ExtractedLayerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        Image.new('RGBA',(20,20),'red').save(self.root/'object.png')
        Image.new('RGBA',(20,20),'green').save(self.root/'repair.png')
        self.track=dict(type='sprite',asset='object.png',repair='repair.png',screenRect=[10,10,10,10],start=0,enter=.24,hold=.32,exit=.28,scale=1.6,offset=[0,0])
    def tearDown(self):self.tmp.cleanup()
    def plan(self,tracks):
        path=self.root/'layers.json';path.write_text(json.dumps(dict(version=1,layers=tracks)));return LayerPlan(path,2,(100,100))
    def source(self):
        im=Image.new('RGB',(100,100),'green');im.paste('red',(20,20,40,40));return im
    def test_clean_repair_and_exact_origin_restoration(self):
        plan=self.plan([self.track]);source=self.source();screen=plan.prepare_screen(source,0)
        self.assertEqual(screen.getpixel((25,25)),(0,128,0))
        frame=screen.convert('RGBA');plan.draw(frame,0,lambda x,y:(x*2,y*2),2)
        self.assertIsNone(ImageChops.difference(frame.convert('RGB'),source).getbbox())
    def test_foreground_can_cross_source_bounds_and_follows_camera(self):
        track=dict(self.track,offset=[-.1,0]);plan=self.plan([track]);frame=Image.new('RGBA',(200,200),'black')
        plan.draw(frame,.4,lambda x,y:(x*4,y*4),4)
        # Native center15*4=60, extraction offset-20 =>40;32point wide =>64outputpx.
        self.assertEqual(frame.getpixel((15,60))[:3],(255,0,0))
        moved=Image.new('RGBA',(200,200),'black');plan.draw(moved,.4,lambda x,y:(x*4+70,y*4),4)
        self.assertNotEqual(moved.getpixel((15,60))[:3],(255,0,0))
        self.assertEqual(moved.getpixel((85,60))[:3],(255,0,0))
    def test_finished_track_does_not_modify_native_screen(self):
        plan=self.plan([self.track]);source=self.source();self.assertIs(plan.prepare_screen(source,1),source)
    def test_glint_uses_current_projection_and_has_no_endpoint_residue(self):
        plan=self.plan([dict(type='glint',start=1,duration=.4,radius=4,anchor=[10,20])])
        before=Image.new('RGBA',(100,100),'black');plan.draw(before,1,lambda x,y:(x+20,y+10),2)
        self.assertEqual(before.getbbox(),(0,0,100,100));self.assertEqual(before.getpixel((30,30))[:3],(0,0,0))
        plan.draw(before,1.2,lambda x,y:(x+20,y+10),2);self.assertGreater(before.getpixel((30,30))[0],150)
    def test_settling_exit_has_one_small_undershoot_and_exact_return(self):
        track=dict(self.track,enter=.14,hold=.06,exit=.5,exitCurve='settle')
        samples=[LayerPlan.progress(track,.20+i*.005) for i in range(101)]
        self.assertEqual(samples[0],1)
        self.assertLess(min(samples),0)
        self.assertGreater(min(samples),-.2)
        self.assertAlmostEqual(samples[-1],0)
        self.assertEqual(sum(a>=0 and b<0 for a,b in zip(samples,samples[1:])),1)
    def test_sheen_is_clipped_to_actual_object_alpha(self):
        source=Image.new('RGBA',(20,20),(255,0,0,0))
        from PIL import ImageDraw
        ImageDraw.Draw(source).ellipse((3,3,16,16),fill='red')
        source.save(self.root/'object.png')
        track=dict(self.track,sheen=dict(start=0,duration=.4,strength=.5))
        plan=self.plan([track])
        # At zero emphasis progress the shadow is absent; sheen changes only real object pixels.
        frame=Image.new('RGBA',(100,100),(0,0,0,0))
        plan.draw(frame,0,lambda x,y:(x*2,y*2),2)
        plain=frame.copy()
        track=dict(track,enter=.0001,hold=.5,scale=1)
        plan=self.plan([track]);frame=Image.new('RGBA',(100,100),(0,0,0,0))
        plan.draw(frame,.2,lambda x,y:(x*2,y*2),2)
        self.assertGreater(frame.getpixel((30,30))[1],0)
        # Far from the object no sweep rectangle is visible.
        self.assertEqual(frame.getpixel((0,0))[3],0)
    def test_invalid_source_geometry_and_nonfinite_times_rejected(self):
        for change in [dict(screenRect=[49,49,10,10]),dict(start=float('nan')),dict(exit=0)]:
            with self.subTest(change=change),self.assertRaises(ValueError):self.plan([dict(self.track,**change)])
if __name__=='__main__':unittest.main()
