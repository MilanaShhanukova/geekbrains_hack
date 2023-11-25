import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ResultTextLayoutComponent } from './result-text-layout.component';

describe('ResultTextLayoutComponent', () => {
  let component: ResultTextLayoutComponent;
  let fixture: ComponentFixture<ResultTextLayoutComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ResultTextLayoutComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ResultTextLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
