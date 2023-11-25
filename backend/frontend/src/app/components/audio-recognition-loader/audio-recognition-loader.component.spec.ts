import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AudioRecognitionLoaderComponent } from './audio-recognition-loader.component';

describe('AudioRecognitionLoaderComponent', () => {
  let component: AudioRecognitionLoaderComponent;
  let fixture: ComponentFixture<AudioRecognitionLoaderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AudioRecognitionLoaderComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(AudioRecognitionLoaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
