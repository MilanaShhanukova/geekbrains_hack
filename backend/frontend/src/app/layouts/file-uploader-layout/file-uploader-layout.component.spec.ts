import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FileUploaderLayoutComponent } from './file-uploader-layout.component';

describe('FileUploaderLayoutComponent', () => {
  let component: FileUploaderLayoutComponent;
  let fixture: ComponentFixture<FileUploaderLayoutComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FileUploaderLayoutComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(FileUploaderLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
